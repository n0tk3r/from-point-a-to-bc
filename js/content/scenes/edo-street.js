// Act Six, the second leg: Osaka, Shinsaibashi-suji at a crossroads, late afternoon (SCENES-21B: new in round twenty-one, in
// place of ENGINE-21's stub; the design, briefs/out/edo2-design.md, sections 5 and 7, #29 and #30; every line is WRITE-21A's,
// js/content/lines/edo-c.en.js, the talks js/content/talk/edo-c.js, S/work-21-writeA/ids.md). The merchant street: Senzō's
// print shop open on the corner (prints pegged on lines, toy prints, the printing bench with its block, its pad and a pot
// of the new blue), the cross street with the town office's fire-watch tower over its roofs, the kelp shop, the medicine
// shop's great signboard ("Uruyusu"), the comb-maker's comb-shaped sign, a water-seller; at the crossroads a small stone road
// god; over the roofs to the right, a theatre's drum tower.
//
// The three of them come up from the Dōjima shore at the left (`shore`), after their supper with O-Natsu, who has gone on to
// the crossroads to ask after her boy:
//   #29 What The Road God Said (Mom)
//     (1) the comb      O-Natsu at the crossroads with her boxwood comb; the custom (Big Sister: "tsuge", to tell); Mom
//                       stands with her and asks her own way, quietly: Jeremiah 31:17 (edo.combAsked)
//     (2) first words   round the corner from down the cross street come the yomiuri pair, and the first words anyone says
//                       are theirs: "...a boy, alive and well, calling for his mother!"
//     (3) the chant     line and line about: a boy's voice at Shosha, in a tongue nobody knows (edo.heardShosha)
//     (4) the men       Kurata and Tatsu round the other corner; the pair run; a sheet flutters down and Big Sister has it
//                       (`sheet`: edo.sheetCaught); Tatsu sees three tall women, and from here he follows them (edo.followed:
//                       the theatre's way opens); Kurata stays at the corner, sighing, until they have gone to the theatre
//     (5) the comb      given to Mom, and O-Natsu's slip for her boy (`comb`, `natsuslip`: edo.combGiven, the beat)
//     Before all that the pair can be seen chanting down the cross street, and a sheet tried for: four mon (a wrong try).
//   #30 Berlin Blue (Big Sister)
//     (1) the marks     Senzō prints one by eye while Big Sister watches: the blue lands a hair to the left, a blurry famous
//                       man ("Every first one is."), and the spoiled sheet goes to Little Sister (`blueprint`); Big Sister
//                       sees the marks cut in the block (edo.marksSeen)
//     (2) the laying    three small places on the bench, in order: the corner mark, the side mark, Senzō's rub (the pad).
//                       Out of order, its own line and a ghost again; in order, a clean print, an actor at home in a robe of
//                       the new blue (edo.registered)
//     (3) the sheet     shown to him once he trusts her hands: he reads it to them, the lock no comb opens (edo.sheetRead)
//   the way on    the right edge to the theatre (the drum tower is its sign), once Tatsu is following them: "Somewhere
//                 dark. Somewhere crowded."; before that, "not yet"
//   the way back  the left edge, to the Dōjima shore
// and a look and a use for each of the three at every thing, and the people's own words.
//
// Every place is PAINT-21C's own measurement of the finished picture (art/scenes/edo-street/layout.json, its ready.md);
// where a place was set by eye against the picture with the people in it, the comment says so.
//
// Try it: index.html?scene=edo-street&lead=mom&flags=edo.landed,edo.paddle,edo.fedPilgrims,edo.vouched,edo.supped

import { natsuStreetTree, senzoTree, LAY, SENZO_TOYAMA } from "../talk/edo-c.js";
import { THREE, who, is, heard, each, lookUse, mine, walkOf, look, swap, giveTo, carries, MATES, dressFor, faceLead, hold, fidget, put,
  walkOff, onLine, talkFor, STOCK_DRESSED } from "./edo-osaka.js";

const art = "art/scenes/edo-street/";

// ---------- the marks (layout.json marks and stands; horizon 262, full 590) ----------
const M = {
  shore: [14, 549], crossroads: [407, 483], roadgod: [278, 495], natsu: [316, 487], prints: [43, 521], bench: [179, 502], senzo: [163, 450],
  medicine: [664, 445], combshop: [775, 443], kelpshop: [583, 456], komuso: [576, 453], watervendor: [752, 456],
  yomiuriFrom: [266, 411], yomiuri2From: [307, 404], yomiuriTo: [431, 477], yomiuri2To: [464, 468],
  kurataFrom: [788, 442], kurataTo: [529, 471], tatsuFrom: [788, 452], tatsuTo: [577, 472], theatre: [786, 437],
};
const SHORE_AT = { mom: [40, 536], bigsis: [64, 545], lilsis: [30, 560] };      // stands shore_<who>
const SENZO_SCALE = 0.655;                                                     // (stands.senzo: on the raised floor, 45 cm up)
// Mom beside O-Natsu at the corner, the two of them before the road god (set by eye: a step to her right, a little nearer)
const MOM_BY_NATSU = [352, 494];
// Little Sister at the bench for the spoiled print, a step in front of Big Sister and to her right (clear of the road god)
const LIL_BY_BENCH = [222, 522];
// where the pair run to (off the right edge, along the street, away from the men coming round the other corner)
const RUN_OFF = [[600, 500], [830, 520]];

// ---------- what the street is doing that is not saved (made again whenever the scene is built) ----------
export const street = { lay: 0, komusoAt: 12000 };

// ---------- #29: the crossroads (O-Natsu's street tree, and its hooks) ----------
const NATSU = natsuStreetTree({
  // Mom beside her, bowing her head, her hands folded, while O-Natsu holds up her comb
  pray: async (g) => {
    const mom = g.actor("mom");
    if (mom && (Math.abs(mom.x - MOM_BY_NATSU[0]) > 6 || Math.abs(mom.y - MOM_BY_NATSU[1]) > 6)) await g.walkTo(MOM_BY_NATSU[0], MOM_BY_NATSU[1], "mom");
    if (mom) { mom.face("W"); mom.pray(); }
    look(g, "natsu", g.view.cast.get("natsu") ? [278, 470] : null);
    hold(g, "natsu", "comb");
    for (const id of ["bigsis", "lilsis"]) look(g, id, "natsu");
    await g.wait(700);
  },
  // the yomiuri pair round the corner from down the cross street, chanting in turn
  sellers: async (g) => {
    const mom = g.actor("mom");
    if (mom) mom.pray(false);
    const a = g.actor("yomiuri1"), b = g.actor("yomiuri2");
    hold(g, "yomiuri1", "chant"); hold(g, "yomiuri2", "chant");
    await Promise.all([a ? walkOf(g, "yomiuri1", [M.yomiuriTo]) : null, b ? g.wait(300).then(() => walkOf(g, "yomiuri2", [M.yomiuri2To])) : null]);
    for (const id of ["yomiuri1", "yomiuri2"]) { const s = g.actor(id); if (s) s.face("SW"); }
    for (const id of [...THREE, "natsu"]) look(g, id, M.yomiuriTo);
  },
  // Kurata and Tatsu round the other corner; the pair run as they are told to; a sheet flutters down, and Big Sister has it
  // before it lands; Kurata goes on, and Tatsu stays, looking at three tall women in hats (the moments under the tree's own
  // lines are staged as each line comes: onLine)
  men: async (g) => {
    const k = await put(g, "kurata", "kurata", M.kurataFrom, "W", { fadeIn: 300 }), t = await put(g, "tatsu", "tatsu", M.tatsuFrom, "W", { fadeIn: 300 });
    await Promise.all([walkOf(g, "kurata", [M.kurataTo]), g.wait(350).then(() => walkOf(g, "tatsu", [M.tatsuTo]))]);
    look(g, "kurata", M.yomiuriTo); look(g, "tatsu", "mom");
    for (const id of ["yomiuri1", "yomiuri2"]) look(g, id, M.kurataTo);
    void k; void t;
    onLine(g, "edo.street.men.2", () => {                                      // "Run." ... "Running."
      for (const id of ["yomiuri1", "yomiuri2"]) { hold(g, id, null); if (g.actor(id)) walkOff(g, id, RUN_OFF, { hurry: true }); }
    });
    onLine(g, "edo.street.men.4", () => {                                      // "Got it. ...I can't read a word of it."
      const big = g.actor("bigsis");
      if (big) { big.face("N"); if (big.hold) big.hold(true, "sheet"); }
      giveTo(g, "bigsis", "sheet");
    });
    onLine(g, "edo.street.men.5", () => { const k = g.actor("kurata"); if (k) { k.face("E"); fidget(g, "kurata", "wearysigh"); } });
    onLine(g, "edo.street.men.6", () => hold(g, "tatsu", "peer"));
  },
  // she presses the comb into Mom's hands, and then the slip for her boy
  gift: async (g) => {
    // (whatever was still under way of the men's moment is finished: the pair gone, the sheet Big Sister's, Kurata at the
    // corner, Tatsu staring at the three of them)
    for (const id of ["yomiuri1", "yomiuri2"]) g.view.cast.remove(id);
    const k = g.actor("kurata");
    if (k) { k.place(M.kurataTo[0], M.kurataTo[1], g.sizeAt(M.kurataTo[0], M.kurataTo[1])); k.face("E"); }
    giveTo(g, "bigsis", "sheet");
    hold(g, "bigsis", null);
    const t = g.actor("tatsu");
    if (t) { t.place(M.tatsuTo[0], M.tatsuTo[1], g.sizeAt(M.tatsuTo[0], M.tatsuTo[1])); look(g, "tatsu", "mom"); if (t.hold) t.hold(true, "peer"); }
    const mom = g.actor("mom");
    if (mom) { mom.pray(false); look(g, "mom", "natsu"); }
    look(g, "natsu", "mom");
    hold(g, "natsu", null);
    await g.wait(300);
    swap(g, "natsu", "natsu-nocomb");                                           // (the comb out of her hair, and into Mom's hands)
    if (mom) hold(g, "mom", "comb");
    giveTo(g, "mom", "comb");
    giveTo(g, "mom", "natsuslip");
    await g.wait(700);
    if (mom) hold(g, "mom", null);
  },
});
async function natsuTalk(g) {
  faceLead(g, "natsu");
  await g.talk(NATSU);
}

// ---------- #29: the yomiuri pair, before they come round the corner ----------
/** Down the cross street, chanting to the people there: a sheet tried for (four mon; Little Sister has one, and it is a
    souvenir), the first time; after that, the price again. */
const sellersUse = Object.assign(async (g) => {
  faceLead(g, "yomiuri2");
  await g.say("edo.street.buy.1");
  if (!heard(g, "edo.street.buy.2")) { look(g, "lilsis", "yomiuri2"); await g.say("edo.street.buy.2"); }
}, { lines: ["edo.street.buy.1", "edo.street.buy.2"] });

// ---------- #30: the print shop (Senzō's tree, its hooks, and the laying) ----------
/** Senzō's demonstration: one sheet by eye, the blue a hair to the left: a blurry famous man ("Every first one is."), and
    the spoiled sheet to Little Sister (WRITE-21A's LAY.ghost, said here, where the design's "the first one always does"
    puts it: the laying after is the player's, and every ghost after it is "again"). */
async function printByEye(g) {
  const s = g.actor("senzo"), p = g.plane("print");
  hold(g, "senzo", "rub");
  await g.wait(900);
  hold(g, "senzo", null);
  if (p) await g.fadePlane("print", "ghost", { ms: 500 });
  // Little Sister comes over to see it (it will be hers), saying what it is on the way
  const lil = who(g) !== "lilsis" ? g.actor("lilsis") : null;
  const coming = lil && Math.hypot(lil.x - LIL_BY_BENCH[0], lil.y - LIL_BY_BENCH[1]) > 12 ? g.walkTo(LIL_BY_BENCH[0], LIL_BY_BENCH[1], "lilsis") : null;
  if (!coming) look(g, "lilsis", M.bench);
  await g.say(LAY.ghost[0]);
  if (coming) { await coming; look(g, "lilsis", M.bench); }
  await g.say(LAY.ghost[1]);
  if (s) hold(g, "senzo", "show");
  await g.say(LAY.ghost[2]);
  giveTo(g, "lilsis", "blueprint");
  if (s) hold(g, "senzo", null);
}
const SENZO = senzoTree({
  watch: async (g) => {
    const big = g.actor("bigsis");
    if (big && who(g) !== "bigsis") await g.walkTo(M.bench[0], M.bench[1], "bigsis");
    if (big) big.face("N");
    if (!carries(g, "lilsis", "blueprint")) await printByEye(g);
  },
  // he draws the shop's curtain a little across the front before he reads (a glance up the street and down, and the sheet
  // held close in both hands)
  curtain: async (g) => {
    const s = g.actor("senzo");
    if (s) { s.face("SE"); await g.wait(400); s.face("SW"); await g.wait(400); s.face("S"); }
    hold(g, "bigsis", null);
    hold(g, "senzo", "read");
    await g.wait(500);
  },
});
async function senzoTalk(g) {
  faceLead(g, "senzo");
  await g.talk(SENZO);
  hold(g, "senzo", null);
}
/** Sōshichi's print shown to Senzō (whoever carries it: Little Sister). */
async function senzoToyama(g) {
  faceLead(g, "senzo");
  if (who(g) === "lilsis") hold(g, "lilsis", "print");
  await g.say(...SENZO_TOYAMA);
  hold(g, "lilsis", null);
}
/** The laying (Big Sister, once she has seen the marks): the corner mark, the side mark, then Senzō's rub. Out of order:
    the step's own line, and a ghost again; in order: a clean print (edo.registered). Before the marks are seen, and for
    Mom and Little Sister, each place is its plain use. */
function lay(step) {
  const fn = async (g) => {
    const me = who(g);
    if (me !== "bigsis" || !is(g, "edo.marksSeen") || is(g, "edo.registered")) return g.say(`edo.street.${step}.use.${me}`);
    const big = g.lead;
    if (big) big.face("N");
    if (step === "cornermark") {
      if (big && big.hold) big.hold(true, "showsheet");
      await g.say(LAY.corner);
      street.lay = 1;
      return;
    }
    if (step === "sidemark") {
      if (street.lay === 1) { await g.say(LAY.side); street.lay = 2; return; }
      await g.say(LAY.sideFirst);
      return spoil(g);
    }
    // the rub (the pad): Senzō's
    if (big && big.hold) big.hold(false);
    if (street.lay === 0) { await g.say(LAY.rubFirst); return spoil(g, true); }
    hold(g, "senzo", "rub");
    await g.say(LAY.rub);
    hold(g, "senzo", null);
    if (street.lay === 1) return spoil(g, false, true);
    // in order: a clean print
    await g.fadePlane("print", "clean", { ms: 600 });
    hold(g, "senzo", "show");
    await g.say(...LAY.good);
    hold(g, "senzo", null);
    street.lay = 0;
    g.flag("edo.registered", true);
  };
  fn.lines = THREE.map((w) => `edo.street.${step}.use.${w}`);
  return fn;
}
/** Out of order: a ghost again (Senzō, by eye, when the rub came first: he lays it himself), and from the corner again. */
async function spoil(g, byEye = false, rubbed = false) {
  const big = g.actor("bigsis");
  if (big && big.hold) big.hold(false);
  if (byEye || !rubbed) { hold(g, "senzo", "rub"); await g.wait(700); hold(g, "senzo", null); }
  street.lay = 0;
  await g.fadePlane("print", "ghost", { ms: 300 });
  await g.say(LAY.again);
}

/** The block: once Big Sister has seen the marks, her look at it is about them. */
const blocksLook = Object.assign((g) => g.say(who(g) === "bigsis" && is(g, "edo.marksSeen") ? "edo.street.blocks.marks.bigsis" : mine(g, "edo.street.blocks")),
  { lines: [...THREE.map((w) => `edo.street.blocks.${w}`), "edo.street.blocks.marks.bigsis"] });

// ---------- the people of the street, used ----------
const kurataUse = (g) => g.say(mine(g, "edo.street.kurata.use"));
kurataUse.lines = THREE.map((w) => `edo.street.kurata.use.${w}`);
const tatsuUse = (g) => g.say(mine(g, "edo.street.tatsu.use"));
tatsuUse.lines = THREE.map((w) => `edo.street.tatsu.use.${w}`);
/** The medicine signboard: the first time anyone tries it, Little Sister sounds it out; then each her own. */
const medicineUse = Object.assign(async (g) => {
  if (!heard(g, "edo.street.medicine.1")) {
    look(g, "lilsis", M.medicine); look(g, "bigsis", "lilsis");
    return g.say("edo.street.medicine.1", "edo.street.medicine.2", "edo.street.medicine.3");
  }
  await g.say(mine(g, "edo.street.medicine.use"));
}, { lines: ["edo.street.medicine.1", "edo.street.medicine.2", "edo.street.medicine.3", ...THREE.map((w) => `edo.street.medicine.use.${w}`)] });

// ---------- the ways ----------
/** The right edge, to the theatre (the drum tower is its sign): once Tatsu is following them. */
async function theatreUse(g) {
  const me = who(g);
  if (!is(g, "edo.followed")) return g.say(`edo.street.theatre.notyet.${me}`);
  await g.say(`edo.street.theatre.go.${me}`);
  await g.goto("edo-theatre", { spawn: "back" });
}
theatreUse.lines = THREE.flatMap((w) => [`edo.street.theatre.notyet.${w}`, `edo.street.theatre.go.${w}`]);

// ---------- now and then: the komusō's few notes ----------
function tick(g, dt) {
  if (!g.scene || g.scene.id !== "edo-street" || g.busy || g.dialogue.active || !g.life || !g.life.enabled) return;
  if ((street.komusoAt -= dt) > 0) return;
  street.komusoAt = 16000 + Math.random() * 14000;
  g.sfx("komuso");
  fidget(g, "komuso", "fluteplay");
}

// ---------- the scene ----------
const thing = (id, name, shape, walkTo, face, more = {}) => ({ id, name, ...shape, walkTo, face, ...lookUse("edo.street", id), ...more });
const chanting = (g) => !is(g, "edo.sheetCaught");
/** Kurata and Tatsu at the corner after the pair have run, until the three of them have gone to the theatre (Tatsu after
    them, round the front: he is in its audience). */
const magistrate = (g) => is(g, "edo.followed") && !is(g, "edo.backstage");

export default {
  id: "edo-street",
  era: "edo",
  name: "Shinsaibashi-suji",
  music: "edo-city",

  // DEPTH (layout.json: horizon 262, full 590, the eye 3.59 m up): one floor, the main street to just before the far side's
  // gutter, and the mouth of the cross street (the shops' fronts are hotspots, not walked into)
  horizon: 262, full: 590,
  walk: { area: [[0, 596], [800, 596], [800, 422], [735, 430], [663, 439], [583, 449], [494, 459], [462, 451], [337, 400], [205, 411], [267, 473], [269, 487], [187, 497], [98, 508], [0, 520]] },
  // the signboard's feet, the road god, the water-seller and his buckets (layout.json blocked)
  blocked: [[[642, 442], [668, 439], [658, 436], [632, 439]], [[234, 495], [272, 491], [262, 482], [226, 486]], [[708, 451], [761, 444], [739, 439], [687, 446]]],

  party: THREE,
  spawn: { default: M.shore, ...M, shore_mom: SHORE_AT.mom, shore_bigsis: SHORE_AT.bigsis, shore_lilsis: SHORE_AT.lilsis, ...SHORE_AT },
  arrive: { shore: [SHORE_AT.bigsis, SHORE_AT.lilsis], theatre: [[760, 452], [770, 470]] },
  facing: "E",
  exits: ["edo-dojima", "edo-theatre"],
  edges: {
    W: { to: "edo-dojima", spawn: "town", name: "back to the shore" },
    E: { to: "edo-theatre", spawn: "back", name: "to the theatre", use: theatreUse },
  },
  stock: STOCK_DRESSED,
  talk: talkFor({
    bigsis: { mom: [{ when: (g) => is(g, "edo.heardShosha"), say: ["edo.street.talk.bigsis.mom.voice.a", "edo.street.talk.bigsis.mom.voice.b"] }] },
    lilsis: { mom: [{ when: (g) => is(g, "edo.heardShosha"), say: ["edo.street.talk.lilsis.mom.comb.a", "edo.street.talk.lilsis.mom.comb.b"] }] },
  }),
  tick,

  picture: art + "back.png",
  // CUT-OUTS, back to front (PAINT-21C's plan): the two lines of prints across the print shop's open front, the three shops'
  // noren, the bench and the sheet on its stand (blank; the blue a ghost; clean), the medicine shop's signboard, the road god,
  // the water-seller
  planes: [
    { id: "prints-1", src: art + "prints-1.png", base: [[-68, 518], [290, 476]] },
    { id: "prints-2", src: art + "prints-2.png", base: [[-68, 518], [290, 476]] },
    { id: "noren-kelp", src: art + "noren-kelp.png", base: [[490, 452], [612, 438]] },
    { id: "noren-med", src: art + "noren-med.png", base: [[616, 438], [704, 427]] },
    { id: "noren-comb", src: art + "noren-comb.png", base: [[707, 427], [803, 416]] },
    { id: "bench", src: art + "bench.png", base: [[100, 499], [250, 482]] },
    { id: "print", states: { blank: art + "print.png", ghost: art + "print-ghost.png", clean: art + "print-clean.png" },
      state: (g) => (is(g, "edo.registered") ? "clean" : is(g, "edo.marksSeen") ? "ghost" : "blank"), base: [[100, 499.2], [250, 482.2]] },
    { id: "sign", src: art + "sign.png", base: [[636, 441], [667, 438]] },
    { id: "roadgod", src: art + "roadgod.png", base: [[232, 494], [270, 489]] },
    { id: "watervendor", src: art + "watervendor.png", base: [[707, 451], [760, 444]] },
    { id: "near", src: art + "near.png", plane: "front" },
  ],
  // THINGS THAT MOVE BY NATURE (layout.json fx): the prints and the noren stirring; two birds wheeling high
  fx: [
    { id: "prints-1-sway", type: "sway", plane: "prints-1", anchor: "top", amount: 1.2, period: 2.6, wave: 18, lean: 0.2 },
    { id: "prints-2-sway", type: "sway", plane: "prints-2", anchor: "top", amount: 1.0, period: 3.1, wave: 16, lean: 0.2 },
    { id: "noren-kelp-sway", type: "sway", plane: "noren-kelp", anchor: "top", amount: 1.6, period: 3.4, wave: 24, lean: 0.3 },
    { id: "noren-med-sway", type: "sway", plane: "noren-med", anchor: "top", amount: 1.8, period: 3.8, wave: 24, lean: 0.3 },
    { id: "noren-comb-sway", type: "sway", plane: "noren-comb", anchor: "top", amount: 1.6, period: 3.0, wave: 22, lean: 0.3 },
    { id: "birds", type: "birds", plane: "back", circle: { at: [470, 70], r: [70, 24] }, count: 2, speed: 12, size: 9, color: "#3a3a4a" },
  ],

  // The people of the street (PEOPLE-21A's kinds, at the painter's marks): O-Natsu at the crossroads (her comb in her hair until
  // she gives it), Senzō kneeling at his bench on the raised floor (at the painter's scale), the komusō playing at a door, the
  // yomiuri pair chanting down the cross street until they come round the corner (and run), Tatsu at the corner once he is
  // following the three of them.
  actors: [
    { id: "natsu", kind: "natsu", at: M.natsu, face: "W", when: (g) => is(g, "edo.supped") && !is(g, "edo.combGiven"), life: { fidget: [6, 12], still: true } },
    { id: "natsu", kind: "natsu-nocomb", at: M.natsu, face: "W", when: (g) => is(g, "edo.combGiven"), life: { fidget: [6, 12], still: true } },
    { id: "senzo", kind: "senzo", at: M.senzo, scale: SENZO_SCALE, face: "S", solid: false, life: { fidget: [5, 10], still: true } },
    { id: "komuso", kind: "komuso-play", at: M.komuso, face: "N", life: { fidget: [8, 16], still: true } },
    { id: "yomiuri1", kind: "yomiuri1", at: M.yomiuriFrom, face: "S", when: chanting, life: { fidget: [3, 7], still: true } },
    { id: "yomiuri2", kind: "yomiuri2", at: M.yomiuri2From, face: "S", when: chanting, life: { fidget: [3, 7], still: true } },
    { id: "tatsu", kind: "tatsu", at: M.tatsuTo, face: "W", when: magistrate, life: { fidget: [6, 12], still: true } },
    { id: "kurata", kind: "kurata", at: M.kurataTo, face: "E", when: magistrate, life: { fidget: [8, 16], still: true } },
  ],

  // Back to front: a later area lies over an earlier one (the other two first: edo-hills.js MATES).
  hotspots: [
    ...MATES,
    thing("roofs", "roofs", { rect: [0, 120, 800, 70] }, M.crossroads, "N"),
    thing("drumtower", "drum tower", { rect: [662, 92, 57, 107] }, M.theatre, "E"),
    thing("firetower", "fire-watch tower", { rect: [272, 51, 70, 156] }, M.crossroads, "N"),
    thing("kelpshop", "kelp shop", { poly: [[488, 452], [610, 438], [610, 315], [488, 320]] }, M.kelpshop, "N"),
    thing("noren", "noren", { rect: [493, 322, 116, 38] }, M.kelpshop, "N"),
    thing("medicine", "medicine signboard", { rect: [635, 321, 31, 122] }, M.medicine, "N", { use: medicineUse }),
    thing("combsign", "comb-maker's sign", { rect: [745, 309, 49, 35] }, M.combshop, "N"),
    thing("watervendor", "water-seller", { rect: [695, 365, 56, 84] }, M.watervendor, "N"),
    thing("crossroads", "crossroads", { poly: [[305, 536], [589, 493], [382, 408], [191, 424]] }, M.crossroads, "N"),
    thing("roadgod", "road god", { rect: [228, 446, 40, 50] }, M.roadgod, "N"),
    thing("printshop", "print shop", { poly: [[0, 509], [248, 480], [248, 325], [0, 334]] }, M.prints, "N"),      // (PAINT-21C's shape, from the picture's edge)
    thing("printlines", "actor prints", { rect: [3, 351, 221, 37] }, M.prints, "N"),
    thing("toyprints", "toy prints", { rect: [1, 380, 125, 35] }, M.prints, "N"),
    // the printing bench and its small things (#30's three places: generous areas round PAINT-21C's small shapes)
    thing("bench", "printing bench", { rect: [108, 405, 137, 65] }, M.bench, "N"),
    thing("blocks", "printing block", { rect: [134, 424, 48, 26] }, M.bench, "N", { look: blocksLook }),
    thing("cornermark", "corner mark", { rect: [132, 428, 17, 21] }, M.bench, "N", { use: lay("cornermark") }),
    thing("sidemark", "side mark", { rect: [164, 428, 17, 21] }, M.bench, "N", { use: lay("sidemark") }),
    thing("baren", "rubbing pad", { rect: [181, 426, 20, 22] }, M.bench, "N", { use: lay("baren") }),
    thing("bluepot", "pot of blue", { rect: [202, 427, 14, 18] }, M.bench, "N"),
    { id: "printsheet", name: "sheet on its stand", rect: [213, 402, 30, 38], walkTo: M.bench, face: "N", use: each("edo.street.printsheet.use"),
      look: Object.assign((g) => g.say(`edo.street.printsheet${is(g, "edo.registered") ? ".clean" : is(g, "edo.marksSeen") ? ".ghost" : ""}.${who(g)}`),
        { lines: THREE.flatMap((w) => [`edo.street.printsheet.${w}`, `edo.street.printsheet.ghost.${w}`, `edo.street.printsheet.clean.${w}`]) }) },
    // the people (the game draws them; their areas go with them)
    { id: "senzo", name: "Senzō", verb: "Talk to", rect: [147, 383, 33, 67], walkTo: M.bench, face: "N", look: each("edo.street.senzo"), use: senzoTalk,
      useWith: { toyamaprint: senzoToyama, sheet: senzoTalk, blueprint: senzoTalk } },
    { id: "natsu", name: "O-Natsu", verb: "Talk to", rect: [300, 395, 31, 92], walkTo: [356, 500], face: "W", look: each("edo.street.natsu"), use: natsuTalk,
      when: (g) => is(g, "edo.supped") },
    { id: "komuso", name: "komusō", rect: [562, 370, 28, 83], walkTo: [560, 480], face: "N", look: each("edo.street.komuso") },      // (a use is a look: he only plays)
    { id: "yomiuri1", name: "broadsheet seller", rect: [254, 356, 24, 56], walkTo: [290, 440], face: "N", look: each("edo.street.yomiuri1"), use: sellersUse, when: chanting },
    { id: "yomiuri2", name: "broadsheet seller", rect: [296, 352, 22, 53], walkTo: [300, 440], face: "N", look: each("edo.street.yomiuri2"), use: sellersUse, when: chanting },
    { id: "tatsu", name: "the staring man", rect: [561, 381, 31, 91], walkTo: [540, 500], face: "E", look: each("edo.street.tatsu"), use: tatsuUse, when: magistrate },
    { id: "kurata", name: "the official", rect: [514, 380, 31, 91], walkTo: [480, 500], face: "E", look: each("edo.street.kurata"), use: kurataUse, when: magistrate },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and whenever the scene is built.
  setup(g) {
    street.lay = 0; street.komusoAt = 12000;
    dressFor(g, "outdoors");
    g.loop("crowd", { level: 0.45 });
    for (const id of ["yomiuri1", "yomiuri2"]) hold(g, id, "chant");
    if (magistrate(g)) hold(g, "tatsu", "peer");
  },

  // The first time up from the shore: the street, and Big Sister at home in it.
  async enter(g) {
    if (is(g, "edo.streetSeen")) return;
    g.flag("edo.streetSeen", true);
    await g.say("edo.street.arrive.1", "edo.street.arrive.2");
  },
};

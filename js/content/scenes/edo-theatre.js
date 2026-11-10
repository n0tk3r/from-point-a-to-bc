// Act Six, the second leg: Osaka, the Inari puppet theatre in the grounds of Naniwa Shrine, backstage, afternoon (SCENES-21B:
// new in round twenty-one, in place of ENGINE-21's stub; the design, briefs/out/edo2-design.md, sections 5 and 7, #31; every
// line is WRITE-21A's, js/content/lines/edo-c.en.js, the talks js/content/talk/edo-c.js, S/work-21-writeA/ids.md). We stand
// backstage, upstage of the stage's left end, and look across the stage to the house: the wing's wall with the back door,
// two black robes and hoods on a peg, a shelf of carved heads over the troupe's boxes, the puppets hanging on their rail;
// the lamp on its stand; the boy puppet on his stand; the black masking curtain; the stage's polished boards and its low set
// (a village gate, a house front); the rail the operators stand behind; beyond it the audience on their mats, row on row; the
// chanter's dais out in the house at stage right.
//
// The three of them come in by the back door (`back`) from Shinsaibashi-suji, Tatsu at their heels round the front:
//   #31 Three To A Puppet (Big Sister and Little Sister; Mom in the audience)
//     the wing        "Somewhere dark. Somewhere crowded." (edo.backstage). Jūbei is in a rage of calm: the last piece of the
//                     day is a boy who runs home to his mother, a puppet takes three, and his left-hand man and his feet man
//                     ran off to Ise yesterday (his tree)
//     (1) black       the robes on the peg: the people who work the left hand and the feet wear black and hoods, and the
//                     house agrees not to see them; the girls offer; "The tall one, the left hand. The small one, the feet.
//                     Robes. Now." (`edo-kurogo`: edo.hooded)
//     (2) rehearsal   each girl tries her one rule once on the doll on its stand (edo.rehearsedLeft, edo.rehearsedFeet:
//                     edo.rehearsed)
//     (3) Mom out front  her use of the audience: round the front through the gap at the wing wall's end, to the only
//                     space left on the mats, next to Tatsu, who offers her his towel (SEAT: edo.momSeated)
//     (4) the show    the stage in the roof hatch's day (the show's painted state, cross-faded in), the doll on the rail with
//                     Jūbei on his stage clogs at its head and the girls at its left hand and its feet (g.troupe); the
//                     chanter's three cues, each kept up while it waits (g.cues): "The boy hears his mother calling" (Big
//                     Sister: his left hand to his ear), "He runs. He runs. He runs for home." (Little Sister: the feet,
//                     stamping), "He kneels down at her door." (both: the hand to the ground, the feet folded). A part done
//                     at the wrong moment: the house laughs at a sad play, Jūbei hisses "Not yet.", and the cue comes round
//                     again (edo.cue1, edo.cue2, edo.cue3). All three: the house weeps, Tatsu weeps, Mom weeps into his towel
//     (5) the troupe  after: Jūbei asks who they are; Mom tells him the true part, and he gives them the road round Osaka:
//                     up the river with the troupe as its carriers, off at Hirakata, the old Yamazaki road (edo.troupeTaken)
//   the way on    once the troupe has taken them and the sheet has been read (#30): "The Kyoto Boat" (cutscenes/edo-boat.js),
//                 told to Jūbei; the back door is the way back to the street, but not while the girls are in black
// and a look and a use for each of the three at every thing, and the people's own words.
//
// Every place is PAINT-21D's own measurement of the finished picture (art/scenes/edo-theatre/layout.json, its ready.md);
// where a place was set by eye against the picture with the people in it, the comment says so.
//
// Try it: index.html?scene=edo-theatre&lead=bigsis&flags=edo.landed,edo.paddle,edo.vouched,edo.supped,edo.combAsked,edo.heardShosha,edo.sheetCaught,edo.followed,edo.combGiven

import { jubeiTree, SEAT, SHOW } from "../talk/edo-c.js";
import { THREE, GIRLS, who, is, heard, each, lookUse, mine, walkOf, look, swap, MATES, dressFor, inBlack, faceLead, hold, talkFor,
  stockFor, STOCK_DRESSED } from "./edo-osaka.js";

const art = "art/scenes/edo-theatre/";

// ---------- the marks (layout.json marks and stands; horizon 190, full 560) ----------
const M = {
  back: [61, 522], jubei: [377, 515], stand: [303, 563], peg: [143, 522], rail: [553, 423], wing: [342, 491], momseat: [408, 410], tatsuseat: [434, 406],
  // (the shamisen player a little to the left of the painter's mark, [661, 361], which is behind the set's house front from here)
  chanter: [625, 350], shamisen: [645, 356], railLeft: [474, 423], railFeet: [517, 424], aisle: [301, 436], gap: [309, 449], lamp: [301, 502],
  boxes: [231, 501], behind: [605, 560],
};
const BACK_AT = { mom: [63, 526], bigsis: [124, 529], lilsis: [62, 561] };            // stands back_<who>
const DAIS = { chanter: 0.486, shamisen: 0.521 };                                     // (stands: on the dais, 45 cm up, at these scales)
// The doll at the rail (layout.json puppet): its place on the operators' floor, between them and the rail; its feet on the
// rail's top, 86 cm up (PEOPLE-21A's PUPPET_RAIL: the kind stands itself on it). The operators at the painter's places,
// as g.troupe's offsets (pixels at full size from the doll's place: (x - 497) / its size there, 0.624).
const PUPPET_AT = [497, 421];
const TROUPE = { head: [89.7, 2], left: [-36.8, 2], feet: [32, 3] };
const FACE = "NW";                                                                      // (the group faces the house, over the rail: we see its back and its left side)
// Rehearsal, backstage: the doll taken off its stand onto PEOPLE-21A's own stand-with-a-doll, where the painted stand is
// (set by eye: its foot under the painted puppet), and the girl whose part it is beside it.
const STAND_AT = [316, 517];
const PRACTISE = { bigsis: [290, 524], lilsis: [338, 524] };
// The girls in the wing, out of their black after the show, either side of the doll back on its stand (Big Sister by the
// lamp, Little Sister between the stand and Jūbei: neither of them behind the doll); Mom back round from the house, through
// the gap, behind them. Big Sister comes down from the rail between the lamp's foot and the stand's.
const AFTER_AT = { mom: [326, 470], bigsis: [264, 503], lilsis: [354, 498] };
const AFTER_VIA = { bigsis: [[330, 490]], lilsis: [] };
// Mom round the front: from the wing to the gap at the wall's end, the aisle, and her place in the front row (the house floor)
const ROUND = { start: [314, 460], via: [M.gap, M.aisle] };

// ---------- what the theatre is doing that is not saved (made again whenever the scene is built) ----------
const SHOW_CUES = { cues: null };
export const showOn = (g) => is(g, "edo.momSeated") && !is(g, "edo.cue3");
/** The stock replies as the story has them now (in black, the girls' looks at each other are the theatre's own). */
function restock(g, scene = g.scene) { if (scene && scene.id === "edo-theatre") scene.stock = stockFor(g, "indoors"); }

// ---------- the wing: Jūbei (his tree, and its hooks) ----------
const JUBEI = jubeiTree({
  // the girls into the black robes and hoods (Little Sister's boots showing); the peg left empty
  robes: async (g) => {
    await Promise.all(GIRLS.map((id, i) => (g.actor(id) ? g.walkTo(M.peg[0] + (i ? 30 : -6), M.peg[1] + (i ? 14 : 2), id) : null)));
    for (const id of GIRLS) { const a = g.actor(id); if (a) a.face("N"); }
    const girls = GIRLS.map((id) => g.actor(id)).filter(Boolean);
    await g.tween(260, (k) => { for (const a of girls) a.fade(1 - k); });
    const p = g.plane("robes");
    if (p) p.show(false);
    for (const id of GIRLS) g.dress(id, "edo-kurogo");
    g.sfx("rustle");
    await g.wait(300);
    for (const a of girls) a.face("E");
    await g.tween(260, (k) => { for (const a of girls) a.fade(k); });
    look(g, "jubei", "bigsis");
  },
  // the girl whose part it is tries it once on the doll on its stand (Big Sister: his left hand to his ear; Little Sister: the
  // feet, stamping); put back as it was when the talk is over (`unpractise`)
  practise: async (g) => {
    const me = who(g) === "lilsis" ? "lilsis" : "bigsis";
    const p = g.plane("boypuppet");
    if (p) p.show(false);
    const doll = g.view.cast.get("rehearsal") || g.view.cast.addFigure("rehearsal", "boypuppet-stand", STAND_AT[0], STAND_AT[1], g.sizeAt(STAND_AT[0], STAND_AT[1])).face("E");
    doll.hidden = false;
    await g.view.cast.load();
    await g.walkTo(PRACTISE[me][0], PRACTISE[me][1], me);
    const girl = g.actor(me);
    if (girl) girl.face(me === "bigsis" ? "E" : "W");
    look(g, "jubei", PRACTISE[me]);
    if (me === "bigsis") {
      await g.pose("rehearsal", "ear");
      if (girl && girl.hold) girl.hold(true, "dollear");
      await g.wait(1300);
    } else {
      if (girl && girl.fidget) girl.fidget("dollrun");
      if (doll.fidget) doll.fidget("dollrun");
      for (const t of [500, 600, 600, 600]) { await g.wait(t); g.sfx("stampfeet"); }
      await g.wait(300);
    }
  },
});
/** Put the rehearsal back: the doll on its painted stand again, the girl's hands down. */
function unpractise(g) {
  g.view.cast.remove("rehearsal");
  const p = g.plane("boypuppet");
  if (p && !showOn(g)) p.show(true);
  for (const id of GIRLS) { const a = g.actor(id); if (a && a.hold && !showOn(g)) a.hold(false); }
}
async function jubeiTalk(g) {
  faceLead(g, "jubei");
  const before = is(g, "edo.troupeTaken");
  await g.talk(JUBEI);
  unpractise(g);
  restock(g);
  if (is(g, "edo.troupeTaken") && is(g, "edo.sheetRead")) {                     // ready: up the river in the morning
    if (!before) await g.say("edo.jubei.bye");                                  // ("Morning. Hachikenya. Don't be late, and don't be noticed.")
    return g.cutscene("edo-boat");
  }
}

// ---------- #31 (3): Mom out front, beside Tatsu ----------
/** Mom's use of the audience, once the girls are hooded and rehearsed: places, girls; round the front through the gap at the
    wing wall's end, along the aisle, to the only space left on the mats, next to Tatsu; down on her knees, sat back; he offers
    her his towel (SEAT: edo.momSeated). Then the show. */
async function takeSeat(g) {
  const me = who(g);
  if (me !== "mom" || !is(g, "edo.rehearsed") || is(g, "edo.momSeated")) return g.say(`edo.theatre.audience.use.${me}`);
  const mom = g.lead;
  for (const id of GIRLS) look(g, id, "mom");
  await g.say(SEAT[0]);                                                          // "Places, girls. I'll be out front ..."
  await g.walkTo(ROUND.start[0], ROUND.start[1]);
  await walkOf(g, "mom", [...ROUND.via, M.momseat]);
  await g.climbTo("momseat", { who: "mom", face: "S" });                         // (onto the house floor: she is in the front row)
  if (mom) { mom.face("S"); mom.kneel("back"); }
  look(g, "tatsu", "mom");
  await g.wait(400);
  await g.say(SEAT[1], SEAT[2]);
  hold(g, "tatsu", "towel");
  await g.say(SEAT[3]);
  await g.wait(400);
  hold(g, "tatsu", null);
  await g.say(SEAT[4], SEAT[5], SEAT[6]);
  g.flag("edo.momSeated", true);
  await beginShow(g);
}

// ---------- #31 (4): the show ----------
/** The cue helper (near.js Cues): three cues of the chanter's, each waiting for the right girl's part. */
function show(g) {
  if (SHOW_CUES.cues) return SHOW_CUES.cues;
  const ops = (name) => { for (const id of ["jubei", "bigsis", "lilsis"]) { const a = g.actor(id); if (a && a.hold) a.hold(true, name); } };
  return (SHOW_CUES.cues = g.cues({ id: "edo.show",
    cues: [
      { line: SHOW.cues[0], who: "bigsis", action: "ear", fact: "edo.cue1", done: async (g) => { ops("dollear"); await g.pose("doll", "ear"); await g.wait(700); } },
      { line: SHOW.cues[1], who: "lilsis", action: "run", fact: "edo.cue2", done: async (g) => {
        for (const id of ["doll", "jubei", "bigsis", "lilsis"]) { const a = g.actor(id); if (a && a.hold) a.hold(false); if (a && a.fidget) a.fidget("dollrun"); }
        for (const t of [520, 580, 580, 580]) { await g.wait(t); g.sfx("stampfeet"); }
        await g.wait(250);
        await g.pose("doll", "run");
        ops("dollrun");
      } },
      { line: SHOW.cues[2], parts: [{ who: "bigsis", action: "ground" }, { who: "lilsis", action: "fold" }], fact: "edo.cue3",
        done: async (g) => { ops("dollkneel"); await g.pose("doll", "kneel"); await g.wait(900); } },
    ],
    // a part at the wrong moment: the house laughs at a sad play, and Jūbei hisses (then the cue comes round again)
    wrong: async (g) => {
      g.sfx("laugh");
      hold(g, "jubei", "hiss");
      await g.say(heard(g, SHOW.wrong[0]) ? SHOW.wrong[1] : SHOW.wrong[0]);
      hold(g, "jubei", "doll");
    },
    done: (g) => afterShow(g),
  }));
}
/** The show's places: the stage in its painted state for the show (the hatch's day, every head in the house turned to the
    stage), the doll on the rail with its three, Jūbei on his stage clogs. `fade`: cross-faded in (else as it is). */
async function stageTheShow(g, fade = true) {
  const p = g.plane("boypuppet");
  if (p) p.show(false);
  swap(g, "jubei", "jubei-stage");
  if (!g.actor("doll")) g.view.cast.addFigure("doll", "boypuppet", PUPPET_AT[0], PUPPET_AT[1], g.sizeAt(PUPPET_AT[0], PUPPET_AT[1]));      // (the doll's own id: "boypuppet" is the cut-out on the stand)
  g.troupe(PUPPET_AT, { doll: "doll", head: "jubei", left: "bigsis", feet: "lilsis", face: FACE, offsets: TROUPE });
  const doll = g.actor("doll");
  if (doll) { doll.hidden = false; doll.fade(1); }
  await g.view.cast.load();
  const ops = (name) => { for (const id of ["jubei", "bigsis", "lilsis"]) { const a = g.actor(id); if (a && a.hold) a.hold(true, name); } };
  // the doll as the cues so far have left him
  const pose = is(g, "edo.cue2") ? "run" : is(g, "edo.cue1") ? "ear" : "stand";
  ops({ stand: "doll", ear: "dollear", run: "dollrun" }[pose]);
  if (pose !== "stand") await g.pose("doll", pose);
  if (fade) {
    const shaft = g.q("#shaft-stage");
    await Promise.all([g.fadePlane("show", 1, { ms: 900 }), g.fadePlane("gate", "show", { ms: 900 }), g.fadePlane("housefront", "show", { ms: 900 }),
      g.tween(900, (k) => { if (shaft) shaft.style.opacity = String(k); })]);
  }
}
async function beginShow(g) {
  for (const id of GIRLS) { const a = g.actor(id); if (a && a.hold) a.hold(false); }
  await stageTheShow(g, true);
  await g.say(SHOW.open);
  await show(g).start(g);
}
/** A part of the doll's, done by the one being played (from where she stands: the girls at the rail, Mom in her seat). The
    left hand is Big Sister's (to his ear; at the kneel, to the ground), the feet Little Sister's (running; at the kneel,
    folded); the other girl's reach for it is Jūbei's hiss of the rule, and Mom watches. Out of the show: the doll's look. */
function part(kind) {
  const fn = async (g) => {
    const me = who(g), s = SHOW_CUES.cues;
    if (!s || !s.on) return g.say(mine(g, "edo.theatre.boypuppet"));
    if (me === "mom") return g.say("edo.theatre.stagerail.use.mom");
    if (kind === "hand" && me !== "bigsis") return g.say("edo.jubei.wrong.lil");
    if (kind === "feet" && me !== "lilsis") return g.say("edo.jubei.wrong.big");
    const action = kind === "hand" ? (s.index === 2 ? "ground" : "ear") : (s.index === 2 ? "fold" : "run");
    await s.answer(g, action);
  };
  fn.lines = ["edo.theatre.stagerail.use.mom", "edo.jubei.wrong.lil", "edo.jubei.wrong.big", ...THREE.map((w) => `edo.theatre.boypuppet.${w}`)];
  return fn;
}
/** "And she opens it.": the house weeps, Tatsu weeps, Mom weeps into his towel; then the stage goes back to the afternoon, the
    girls come down from the rail and out of their black, the doll goes back on his stand, Mom comes back round; and Jūbei
    turns to them (his tree's `after`). */
async function afterShow(g) {
  await g.say(SHOW.end);
  g.sfx("sob");
  hold(g, "tatsu", "weep");
  hold(g, "mom", "weep");
  await g.wait(900);
  await g.say(...SHOW.after);
  hold(g, "tatsu", null);
  g.caption(null);
  await endShow(g);
  await jubeiTalk(g);
}
/** The show over (edo.cue3): the stage as it was, the girls in the wing in their own travel clothes, the doll on its stand,
    Jūbei off his clogs, Mom back round from the house. */
async function endShow(g) {
  const shaft = g.q("#shaft-stage");
  await Promise.all([g.fadePlane("show", 0, { ms: 900 }), g.fadePlane("gate", "before", { ms: 900 }), g.fadePlane("housefront", "before", { ms: 900 }),
    g.tween(900, (k) => { if (shaft) shaft.style.opacity = String(1 - k); })]);
  for (const id of ["doll", "jubei", "bigsis", "lilsis"]) { const a = g.actor(id); if (a && a.hold) a.hold(false); }
  g.view.cast.remove("doll");
  const p = g.plane("boypuppet");
  if (p) p.show(true);
  swap(g, "jubei", "jubei", M.jubei, "W");
  const mom = g.actor("mom");
  if (mom) { mom.hold(false); mom.kneel(false); }
  const girls = GIRLS.map((id) => g.actor(id)).filter(Boolean);
  await Promise.all([
    ...GIRLS.map((id) => (g.actor(id) ? walkOf(g, id, [...AFTER_VIA[id], AFTER_AT[id]]) : null)),
    mom ? (async () => { await g.wait(500); await walkOf(g, "mom", [M.aisle, M.gap, AFTER_AT.mom]); await g.climbTo(AFTER_AT.mom, { who: "mom" }); })() : null,
  ]);
  await g.tween(240, (k) => { for (const a of girls) a.fade(1 - k); });
  dressFor(g, "indoors");                                                        // (edo.cue3: out of their black)
  const robes = g.plane("robes");
  if (robes) robes.show(true);
  await g.tween(240, (k) => { for (const a of girls) a.fade(k); });
  for (const id of THREE) { g.rememberPlace(id); look(g, id, "jubei"); }
  restock(g);
}

// ---------- the wing's things ----------
/** The boy puppet on his stand: once the girls are in black and the show is to come, a reach for his head is a reach for
    Jūbei's own place (the wrong try: "Mine? My face shows."); otherwise each her own. */
const puppetUse = Object.assign(async (g) => {
  const me = who(g);
  if (is(g, "edo.hooded") && !is(g, "edo.momSeated") && me !== "mom") { faceLead(g, "jubei"); return g.say("edo.jubei.own"); }
  await g.say(mine(g, "edo.theatre.boypuppet.use"));
}, { lines: ["edo.jubei.own", ...THREE.map((w) => `edo.theatre.boypuppet.use.${w}`)] });
/** The puppets on their rail: Little Sister's look is a small argument with her sister ("SLEEPING."). */
const puppetsLook = Object.assign(async (g) => {
  if (who(g) !== "lilsis") return g.say(mine(g, "edo.theatre.puppets"));
  if (heard(g, "edo.theatre.puppets.lilsis.3")) return g.say("edo.theatre.puppets.lilsis");
  look(g, "bigsis", "lilsis");
  await g.say("edo.theatre.puppets.lilsis", "edo.theatre.puppets.lilsis.2", "edo.theatre.puppets.lilsis.3");
}, { lines: ["edo.theatre.puppets.mom", "edo.theatre.puppets.bigsis", "edo.theatre.puppets.lilsis", "edo.theatre.puppets.lilsis.2", "edo.theatre.puppets.lilsis.3"] });
/** The back door: the way back to the street, but not while the girls are in black (each her own refusal then). */
const backdoorUse = Object.assign(async (g) => {
  if (inBlack(g)) return g.say(mine(g, "edo.theatre.backdoor.use"));
  await g.goto("edo-street", { spawn: "theatre" });
}, { lines: THREE.map((w) => `edo.theatre.backdoor.use.${w}`) });

// ---------- the scene ----------
const thing = (id, name, shape, walkTo, face, more = {}) => ({ id, name, ...shape, walkTo, face, ...lookUse("edo.theatre", id), ...more });
const STAGE_FLOOR = [[19, 509], [45, 504], [69, 499], [93, 495], [116, 491], [138, 486], [160, 482], [161, 486], [161, 489], [162, 493], [162, 497], [163, 501],
  [163, 505], [184, 501], [204, 497], [224, 493], [244, 489], [262, 485], [281, 481], [279, 478], [277, 474], [275, 471], [273, 467], [271, 464], [270, 461],
  [278, 460], [286, 458], [294, 456], [303, 455], [311, 453], [319, 452], [322, 457], [327, 462], [331, 468], [335, 474], [340, 480], [344, 486], [351, 484],
  [358, 483], [365, 481], [372, 480], [378, 478], [385, 477], [379, 471], [373, 465], [368, 459], [363, 453], [358, 448], [353, 443], [405, 433], [453, 424],
  [498, 415], [540, 407], [578, 400], [615, 393], [619, 395], [623, 397], [627, 399], [632, 400], [636, 402], [641, 404], [637, 406], [632, 407], [628, 409],
  [647, 417], [668, 427], [691, 437], [716, 448], [743, 461], [773, 474], [785, 475], [798, 475], [798, 594], [2, 594], [2, 564], [3, 560]];
const HOUSE_FLOOR = [[274, 429], [306, 424], [337, 418], [367, 413], [396, 409], [423, 404], [449, 400], [452, 402], [456, 404], [459, 406], [462, 408], [466, 410],
  [470, 412], [447, 417], [423, 421], [398, 425], [373, 430], [346, 435], [318, 440], [320, 442], [322, 445], [324, 447], [318, 448], [312, 449], [307, 451],
  [301, 452], [295, 453], [289, 454], [286, 449], [284, 445], [281, 441], [278, 437], [276, 433]];

export default {
  id: "edo-theatre",
  era: "edo",
  name: "The Inari theatre",
  music: "edo-theatre",                                                          // (ENGINE-21's track: a plucked string, low and grave)

  // DEPTH (layout.json: room.View, horizon 190, full 560, the lens 405 cm up): two floors on one level (a hut theatre): the
  // wing, the stage behind the rail and backstage behind it (`stage`); and the house's front aisle and Mom's place in the
  // front row (`house`), reached only by a script (Mom goes round the front: takeSeat)
  horizon: 190, full: 560,
  walk: [{ name: "stage", area: STAGE_FLOOR },
    { name: "house", area: HOUSE_FLOOR, away: { mom: "edo.theatre.audience.use.mom", bigsis: "edo.theatre.audience.use.bigsis", lilsis: "edo.theatre.audience.use.lilsis" } }],
  // the lamp's foot, the stand's foot, the gate's two posts, the boxes at the front (layout.json blocked)
  blocked: [[[269, 478], [300, 472], [309, 485], [277, 492]], [[286, 509], [331, 499], [346, 522], [298, 534]], [[376, 465], [395, 461], [405, 470], [384, 475]],
    [[437, 453], [455, 449], [465, 457], [447, 461]], [[632, 566], [872, 480], [1054, 551], [805, 693]],
    // (round twenty-three: the near plane's post of the wing stands over the walked floor's right end, at the frame's edge)
    [[740, 455], [800, 469], [800, 514], [740, 534]]],

  party: THREE,
  spawn: { default: M.back, ...M, back_mom: BACK_AT.mom, back_bigsis: BACK_AT.bigsis, back_lilsis: BACK_AT.lilsis, ...BACK_AT },
  arrive: { back: [BACK_AT.bigsis, BACK_AT.lilsis] },
  facing: "E",
  exits: ["edo-street"],
  // during the show everyone stays where she is: the girls do their parts from the rail, Mom watches from her seat
  still: (g) => showOn(g),
  stock: STOCK_DRESSED,                                                          // (setup and the show's ends set it from the story: restock)
  talk: talkFor({
    bigsis: { mom: [{ when: (g) => !is(g, "edo.cue3"), say: ["edo.theatre.talk.bigsis.mom.play.a", "edo.theatre.talk.bigsis.mom.play.b"] }] },
    lilsis: { bigsis: [{ when: (g) => !is(g, "edo.cue3"), say: ["edo.theatre.talk.lilsis.bigsis.stamp.a", "edo.theatre.talk.lilsis.bigsis.stamp.b"] }] },
  }),

  picture: art + "back.png",
  // CUT-OUTS, back to front (PAINT-21D's plan): the show's painted state (laid over the backdrop, under every cut-out: the
  // stage in the roof hatch's day, the house turned to it), the robes on their peg, the stage rail, the lamp, the boy puppet on
  // his stand, the masking curtain, the set's gate and house front (each in two states, the show's lit), the boxes in front.
  planes: [
    { id: "show", src: art + "show.png", plane: "back", when: showOn },
    { id: "robes", src: art + "robes.png", plane: "back", when: (g) => !inBlack(g) },
    { id: "stagerail", src: art + "stagerail.png", base: [[344, 439], [609, 389]] },
    { id: "lamp", src: art + "lamp.png", base: 486 },
    { id: "boypuppet", src: art + "boypuppet.png", base: 523, when: (g) => !showOn(g) },
    { id: "curtain", src: art + "curtain.png", base: [[329, 440], [359, 476]] },
    { id: "gate", states: { before: art + "gate.png", show: art + "gate-show.png" }, state: (g) => (showOn(g) ? "show" : "before"), base: [[377, 471], [462, 452]] },
    { id: "housefront", states: { before: art + "housefront.png", show: art + "housefront-show.png" }, state: (g) => (showOn(g) ? "show" : "before"), base: [[778, 467], [651, 407]] },
    { id: "front", src: art + "front.png", plane: "front" },
    { id: "near", src: art + "near.png", plane: "front" },
  ],
  // LIGHT (PAINT-21D's light pictures, laid over the painting with a screen blend, under the people, as the keep's beams are):
  // the right wall's high windows' day in the air; and in the show, the roof hatch's day falling onto the stage
  live(kit, g) {
    const url = (file) => (g && g.assets && g.assets.url ? g.assets.url(art + file) : new URL("../../../" + art + file, import.meta.url).href);
    const on = g && g.store ? showOn(g) : false;
    return `<image id="shaft-house" href="${url("shaft-house.png")}" width="800" height="600" style="mix-blend-mode:screen;image-rendering:pixelated"/>`
      + `<image id="shaft-stage" href="${url("shaft-stage.png")}" width="800" height="600" style="mix-blend-mode:screen;image-rendering:pixelated;opacity:${on ? 1 : 0}"/>`;
  },
  // THINGS THAT MOVE BY NATURE (layout.json fx): the lamp's flame backstage; motes turning in the house's shafts of day
  fx: [
    { id: "lamp-flame", type: "flame", at: [291, 396], size: 7, glow: 22, glowColor: "#f4d88e", glowOpacity: 0.22, flicker: 0.5, base: 486 },
    { id: "dust", type: "birds", plane: "back", lanes: [[[560, 250], [430, 330]], [[600, 240], [470, 340]]], every: [6, 14], group: [1, 2], size: 2, speed: 8, color: "#f6eed8" },
  ],

  // The people of the theatre (PEOPLE-21A's kinds, at the painter's marks): Jūbei in the wing by the boy puppet's stand (on his
  // stage clogs at the doll's head during the show), the chanter and the shamisen player kneeling on their dais out in the
  // house (at the painter's scales), and Tatsu in the front row, cross-legged, a towel ready; during the show, the doll on the
  // rail (PEOPLE-21A's boy puppet, its feet on the rail's top).
  actors: [
    { id: "jubei", kind: "jubei", at: M.jubei, face: "W", when: (g) => !showOn(g), life: { fidget: [6, 12], still: true } },
    { id: "jubei", kind: "jubei-stage", at: M.rail, face: FACE, when: showOn, life: { fidget: false } },
    { id: "doll", kind: "boypuppet", at: PUPPET_AT, face: FACE, solid: false, when: showOn, life: { fidget: false } },
    { id: "chanter", kind: "chanter", at: M.chanter, scale: DAIS.chanter, face: "W", solid: false, life: { fidget: [8, 16], still: true } },
    { id: "shamisen", kind: "shamisen", at: M.shamisen, scale: DAIS.shamisen, face: "W", solid: false, life: { fidget: [5, 10], still: true } },
    { id: "tatsu", kind: "tatsu-seated", at: M.tatsuseat, face: "S", solid: false, life: { fidget: [8, 16], still: true } },
  ],

  // Back to front: a later area lies over an earlier one (the other two first: edo-hills.js MATES).
  hotspots: [
    ...MATES,
    thing("rafters", "rafters", { poly: [[0, 0], [799, 0], [799, 150], [0, 150]] }, M.wing, "N"),
    thing("windows", "high windows", { poly: [[257, 167], [634, 164], [634, 200], [257, 199]] }, M.wing, "N"),
    thing("audience", "audience", { poly: [[221, 303], [444, 286], [589, 366], [280, 416]] }, ROUND.start, "N", { use: takeSeat }),
    // (the boards are the floor the operators walk on: only their near edge is the thing to click, so that a click anywhere
    // else on them walks there; the set's areas stop above the boards for the same reason)
    thing("stage", "stage", { poly: [[478, 576], [800, 468], [800, 482], [482, 592]] }, M.wing, "E"),
    { id: "set", name: "set", rect: [364, 292, 433, 150], walkTo: M.wing, face: "E", use: each("edo.theatre.set.use"),
      look: Object.assign((g) => g.say(`edo.theatre.set${showOn(g) ? ".show" : ""}.${who(g)}`), { lines: THREE.flatMap((w) => [`edo.theatre.set.${w}`, `edo.theatre.set.show.${w}`]) }) },
    thing("housefront", "house front", { rect: [637, 292, 160, 150] }, M.rail, "E"),
    thing("gate", "village gate", { rect: [364, 308, 114, 150] }, M.wing, "E"),
    thing("dais", "chanter's dais", { poly: [[537, 338], [604, 330], [724, 364], [724, 386], [649, 401], [537, 357]] }, M.rail, "E"),
    thing("book", "chanter's book", { rect: [593, 324, 33, 19] }, M.rail, "E"),
    thing("stagerail", "stage rail", { poly: [[343, 437], [345, 387], [607, 346], [612, 348], [607, 389], [345, 440]] }, M.rail, "N"),
    thing("curtain", "curtain", { rect: [328, 81, 33, 382] }, M.wing, "E"),
    thing("puppets", "puppets", { rect: [-2, 265, 302, 67] }, M.peg, "N", { look: puppetsLook }),
    thing("heads", "carved heads", { rect: [178, 351, 76, 18] }, M.boxes, "N"),
    thing("boxes", "boxes", { rect: [174, 432, 96, 45] }, M.boxes, "N"),
    { id: "robes", name: "black robes", rect: [103, 354, 55, 82], walkTo: M.peg, face: "N", use: each("edo.theatre.robes.use"),
      look: Object.assign((g) => g.say(`edo.theatre.robes${inBlack(g) ? ".worn" : ""}.${who(g)}`), { lines: THREE.flatMap((w) => [`edo.theatre.robes.${w}`, `edo.theatre.robes.worn.${w}`]) }) },
    thing("backdoor", "back door", { rect: [10, 353, 88, 132] }, M.back, "W", { use: backdoorUse, verb: "Go out by" }),
    thing("lamp", "lamp", { rect: [276, 397, 26, 91] }, M.lamp, "N"),
    thing("stand", "puppet's stand", { rect: [291, 415, 51, 105] }, M.lamp, "E"),
    thing("boypuppet", "boy puppet", { rect: [300, 414, 33, 79] }, M.lamp, "E", { use: puppetUse, when: (g) => !showOn(g) }),
    // the doll at the rail, in the show: his left hand (Big Sister's), his feet (Little Sister's)
    { id: "dollhand", name: "the boy's left hand", verb: "Work", rect: [476, 314, 40, 38], look: each("edo.theatre.boypuppet"), use: part("hand"), when: showOn },
    { id: "dollfeet", name: "the boy's feet", verb: "Work", rect: [478, 352, 38, 22], look: each("edo.theatre.boypuppet"), use: part("feet"), when: showOn },
    // the people (the game draws them; their areas go with them)
    { id: "jubei", name: "Jūbei", verb: "Talk to", rect: [352, 390, 50, 125], walkTo: [350, 520], face: "E", look: each("edo.theatre.jubei"), use: jubeiTalk,
      when: (g) => !showOn(g) },
    { id: "chanter", name: "chanter", rect: [617, 312, 15, 38], walkTo: M.rail, face: "E", look: each("edo.theatre.chanter") },
    { id: "shamisen", name: "shamisen player", rect: [637, 318, 16, 40], walkTo: M.rail, face: "E", look: each("edo.theatre.shamisen") },
    { id: "tatsu", name: "the staring man", rect: [425, 360, 18, 46], walkTo: M.rail, face: "N", look: each("edo.theatre.tatsu") },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and whenever the scene is built.
  setup(g) {
    SHOW_CUES.cues = null;
    restock(g, this);
    dressFor(g, "indoors");
    if (showOn(g)) {
      const mom = g.actor("mom");
      if (mom && g.floorOf && (g.floorOf(mom) || {}).name === "house") mom.kneel("back");
    }
  },

  async enter(g) {
    if (!is(g, "edo.backstage")) {
      g.flag("edo.backstage", true);
      await g.say("edo.theatre.arrive.1", "edo.theatre.arrive.2");
      return;
    }
    // a game loaded in the middle of the show: everyone in her place, and the cue waiting is said again
    if (showOn(g) && !(SHOW_CUES.cues && SHOW_CUES.cues.on)) {
      await stageTheShow(g, false);
      const s = show(g);
      s.index = s.first(g); s.got.clear(); s.on = s.index < s.list.length;
      if (s.on) g.caption(s.cue.line);
    }
  },
};

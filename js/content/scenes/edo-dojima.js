// Act Six, the second leg: Osaka, the Dōjima shore (SCENES-21B: new in round twenty-one, in place of ENGINE-21's stub; the
// design, briefs/out/edo2-design.md, sections 5 and 7, #28; every line is WRITE-21A's, js/content/lines/edo-c.en.js, the
// talks js/content/talk/edo-c.js, and S/work-21-writeA/ids.md says when each is said). The rice dealers' quarter on the
// river, the last week of April 1830, the pilgrimage in flood, about four in the afternoon: O-Natsu's house front and her
// alms stall (the great rice pot on its hearth, the tub of pickled radish, the tray of rice balls, the sandals, the kettle),
// the pilgrims' line with their ladles, the stone steps down to the water where the lighter left the family, the river
// busy with lighters, the domains' white warehouses across it, a high timber bridge, far up the river a castle with no keep,
// and at the right the rice market spilling into the road after the close: the dealers, the water men with their buckets.
//
// The three of them land here (the Uttermost Parts, SCENES-21A's edo-sail.js, ends on the mark `landing`; LEG_START.osaka):
//   the landing   they come up the river steps (faded in at their top: the floor cannot go down them, PAINT-21C) as the
//                 lighter pulls away (its cut-out goes), and say where they are (WRITE-21A's LANDING) (edo.landed)
//   #28 The Dōjima Shore
//     (1) no ladle    the stall used before the paddle: a kind look and a shake of the head; the first time, Little Sister's
//                     plan ("We could BORROW a ladle." "And then we'd be lying with a spoon."); Kyūhachi's ladle for a
//                     share (his tree): "No, thank you."
//     (2) the paddle  Mom asks O-Natsu if she can help (her tree): O-Natsu hands her the rice paddle (`paddle`): the
//                     kitchen is hers (edo.paddle)
//     (3) serving     a job each, behind the stall, by the right one of them (the wrong one: "That's somebody else's job."):
//                     Mom at the pot (edo.potServed), Big Sister shaping rice balls with salted hands (edo.ballsShaped: the
//                     tray half full), Little Sister handing out the pickle, a slice each (edo.pickleServed); the man who
//                     comes round again steps up to her tub, and the second time she is at it she catches him on his fifth
//                     (FIFTH: edo.fifthCaught). All three: the line fed (edo.fedPilgrims), and the pilgrims go on east
//     (4) "My helpers."  Kurata the dōshin comes along the line with Tatsu and asks who these three are; O-Natsu: "My
//                     helpers." He takes a rice ball, looks at it, and goes on; Tatsu stares, and follows him (VOUCH:
//                     edo.vouched, the beat)
//     (5) the supper  O-Natsu's tree, straight after: the helpers sit on the river steps with the last of the pot; Little
//                     Sister's grace; the paddle given back (edo.supped); O-Natsu asks Mom to come to the crossroads
//   the way on    the right edge into the town (the merchant street, edo-street.js) once they have eaten with her; before
//                 the paddle "Not yet." (nobody walks a city hungry), and before the supper "Not without thanking her."
//   the way back  the steps: the lighter has gone
// and a look and a use for each of the three at every thing, and the people's own words.
//
// Every place is PAINT-21C's own measurement of the finished picture (art/scenes/edo-dojima/layout.json, its ready.md);
// where a place was set by eye against the picture with the people in it, the comment says so.
//
// Try it: index.html?scene=edo-dojima&lead=mom (dressed by script as LEG_START.osaka has them: edo-common.js)

import { natsuTree, riheiTree, kyuhachiTree, VOUCH, FIFTH, LANDING } from "../talk/edo-c.js";
import { THREE, who, is, heard, each, lookUse, mine, walkOf, look, giveTo, takeFrom, MATES, dressFor, faceLead, nth, hold, fidget,
  walkOff, sitOnStep, standFromStep, talkFor, STOCK_DRESSED } from "./edo-osaka.js";

const art = "art/scenes/edo-dojima/";

// ---------- the marks (layout.json marks and stands; horizon 262, full 590) ----------
const M = {
  landing: [479, 461], steps: [481, 457], stall: [154, 490], natsu: [350, 464], pot: [209, 456], balls: [265, 460], pickle: [311, 463],
  line1: [215, 493], line2: [235, 513], line3: [261, 538], line4: [300, 570], kyuhachi: [390, 560], market: [687, 496], rihei: [703, 480],
  watermen: [548, 481], kurataFrom: [784, 524], kurataTo: [341, 500], tatsuFrom: [770, 541], tatsuTo: [382, 514], town: [788, 546],
};
const LANDING_AT = { mom: [479, 461], bigsis: [407, 459], lilsis: [435, 468] };      // stands landing_<who>
// Where the people of the shore are when nobody has moved them (set by eye against the picture, from the painter's marks):
// Kurata and Tatsu walk the shore at the right, looking at faces, until they come along the line (#28, (4)).
const KURATA_AT = [626, 524], TATSU_AT = [668, 542];
// Kyūhachi, his fifth time round: up at the front, before Little Sister's tub (in front of the table, beside the first in line).
const FIFTH_AT = [292, 496];
// The pilgrims go on east, fed, along the shore street and out at the right (by the town's mark).
const EAST = [[560, 560], [760, 560], [830, 560]];
// Their own supper, on the river steps: the three sat along the coping at the top of the flight, their backs to the river,
// facing the street (the feet's places; set by eye: the lip of the bank runs at about row 453 to 457 here).
const SUPPER = { mom: [500, 462], bigsis: [468, 461], lilsis: [438, 461] };

// ---------- what the shore is doing that is not saved (made again whenever the scene is built) ----------
export const shore = { serving: false, splashAt: 8000, splashing: 0, runAt: 18000, running: null };

// ---------- the landing ----------
/** Up the river steps (the floor cannot go down them: they are faded in at the top, PAINT-21C) as the lighter pulls away
    with the bales it brought, and where they are (WRITE-21A's LANDING), once. */
async function landing(g) {
  const lighter = g.plane("lighter"), family = THREE.map((id) => g.actor(id)).filter(Boolean);
  for (const f of family) f.fade(0);
  g.sfx("creak");
  await g.tween(900, (k) => { for (const f of family) f.fade(k); });
  for (const id of THREE) look(g, id, [470, 600]);
  if (lighter) {                                                                // (it slides off downstream, to the right, and is gone)
    lighter.show(true);
    await g.tween(1400, (k) => { lighter.place(60 * k, -4 * k); lighter.fade(1 - k); });
    lighter.show(false);
  }
  g.flag("edo.landed", true);
  if (!heard(g, LANDING[0])) await g.say(...LANDING);
}

// ---------- #28 (1): no ladle ----------
/** The stall, used before the paddle: a kind look and a shake of the head; the first time (by any of them), Little Sister's
    plan and Mom's answer. After the paddle it is the stall they work at: its plain use. */
const stallUse = Object.assign(async (g) => {
  if (is(g, "edo.paddle")) return g.say(mine(g, "edo.dojima.stall.use"));
  const n = g.actor("natsu");
  if (n) { faceLead(g, "natsu"); if (n.fidget) n.fidget("ojigi"); }
  await g.say(mine(g, "edo.dojima.stall.use"));
  if (!heard(g, "edo.dojima.borrow.1")) {
    look(g, "lilsis", "mom"); look(g, "mom", "lilsis");
    await g.say("edo.dojima.borrow.1", "edo.dojima.borrow.2");
  }
}, { lines: [...THREE.map((w) => `edo.dojima.stall.use.${w}`), "edo.dojima.borrow.1", "edo.dojima.borrow.2"] });

// ---------- #28 (2) and (5): O-Natsu ----------
const NATSU = natsuTree({
  // she looks at Mom a moment, and hands her the rice paddle: the kitchen is hers
  paddle: async (g) => {
    const n = g.actor("natsu"), mom = g.actor("mom");
    if (n) { look(g, "natsu", "mom"); hold(g, "natsu", "paddle"); }
    await g.wait(600);
    if (mom && who(g) !== "mom") { await g.walkTo(Math.min(n ? n.x - 26 : 330, 330), 470, "mom"); look(g, "mom", "natsu"); }
    giveTo(g, "mom", "paddle");
    hold(g, "natsu", null);
    if (mom) hold(g, "mom", "paddle");
    await g.wait(500);
    if (mom) hold(g, "mom", null);
  },
  // the helpers sit on the river steps with the last of the pot
  sit: async (g) => {
    hold(g, "natsu", null);
    await Promise.all(THREE.map((id) => (g.actor(id) ? sitOnStep(g, id, SUPPER[id], "S") : null)));
    look(g, "natsu", SUPPER.mom);
  },
  // after Little Sister's grace: they eat, a rice ball each (no table word)
  eat: async (g) => {
    for (const id of THREE) hold(g, id, "riceball");
    await g.wait(1200);
  },
  // the paddle back, clean; and up off the steps
  giveBack: async (g) => {
    for (const id of THREE) hold(g, id, null);
    takeFrom(g, "mom", "paddle");
    await Promise.all(THREE.map((id) => standFromStep(g, id)));
  },
});
async function natsuTalk(g) {
  faceLead(g, "natsu");
  await g.talk(NATSU);
}

// ---------- #28 (3): serving ----------
const TASK = { pot: "mom", tray: "bigsis", tub: "lilsis" };
const TASK_AT = { pot: M.pot, tray: M.balls, tub: M.pickle };
const served = (g) => is(g, "edo.potServed") && is(g, "edo.ballsShaped") && is(g, "edo.fifthCaught");
/** A task at the stall, after the paddle and before the line is fed: by the right one of them, her job (her hold, her
    line); by the wrong one, "That's somebody else's job."; before the paddle, the thing's own use (not hers to touch). */
function task(thing) {
  const fn = async (g) => {
    const me = who(g);
    if (!is(g, "edo.paddle") || is(g, "edo.fedPilgrims")) return g.say(`edo.dojima.${thing}.use.${me}`);
    if (TASK[thing] !== me) return g.say(`edo.dojima.notmine.${me}`);
    const l = g.lead;
    if (l) l.face("S");
    if (thing === "pot") {
      look(g, "awafather", "mom");
      hold(g, "mom", "serve");
      await g.say("edo.dojima.serve.mom");
      hold(g, "mom", null);
      g.flag("edo.potServed", true);
    } else if (thing === "tray") {
      hold(g, "bigsis", "shape");
      look(g, "natsu", "bigsis");
      await g.say("edo.dojima.balls.1", "edo.dojima.balls.2");
      hold(g, "bigsis", null);
      g.flag("edo.ballsShaped", true);
    } else if (!is(g, "edo.pickleServed")) {
      hold(g, "lilsis", "pickle");
      await g.say("edo.dojima.serve.lilsis");
      hold(g, "lilsis", null);
      g.flag("edo.pickleServed", true);
      await roundAgain(g);                                                       // (the man who comes round again)
    } else if (!is(g, "edo.fifthCaught")) {
      const k = g.actor("kyuhachi");
      if (k) { look(g, "lilsis", "kyuhachi"); hold(g, "kyuhachi", "ladleout"); }
      await g.say(FIFTH[0], FIFTH[1]);
      await g.say(FIFTH[2]);
      look(g, "natsu", "lilsis");
      await g.say(FIFTH[3]);
      hold(g, "lilsis", "pickle");
      await g.wait(500);
      hold(g, "lilsis", null);
      hold(g, "kyuhachi", null);
      g.flag("edo.fifthCaught", true);
      if (k) await walkOf(g, "kyuhachi", [M.kyuhachi]);                          // (back to his place, to try a sixth)
      if (k) k.face("W");
    } else return g.say("edo.dojima.serve.lilsis");
    if (served(g)) await lineFed(g);
  };
  fn.lines = [...THREE.map((w) => `edo.dojima.${thing}.use.${w}`), ...THREE.map((w) => `edo.dojima.notmine.${w}`)];
  return fn;
}
/** Kyūhachi, his fifth time round: from his place up to the front, before Little Sister's tub, his ladle out. */
async function roundAgain(g) {
  const k = g.actor("kyuhachi");
  if (!k || is(g, "edo.fifthCaught")) return;
  await walkOf(g, "kyuhachi", [[360, 520], FIFTH_AT]);
  k.face("N");
  hold(g, "kyuhachi", "ladleout");
}
/** The line fed (all three tasks): the pilgrims thank O-Natsu and go on east; then Kurata comes along the shore with Tatsu
    (VOUCH), "My helpers.", and their own supper (O-Natsu's tree). */
async function lineFed(g) {
  if (is(g, "edo.fedPilgrims")) return;
  look(g, "natsu", "mom");
  await g.say(VOUCH[0]);                                                          // "That's the line. That's the whole line."
  g.flag("edo.fedPilgrims", true);
  const goers = ["awafather", "awamother", "oldpilgrim", "ladleboy"].filter((id) => g.actor(id));
  for (const id of goers) fidget(g, id, "ojigi");
  await g.wait(500);
  await Promise.all(goers.map((id, i) => g.wait(i * 350).then(() => walkOff(g, id, EAST))));
  await vouch(g);
}
/** #28 (4): Kurata the dōshin along the shore to the stall, Tatsu at his back; "...Who are these three?" "My helpers."; a rice
    ball taken and looked at; on he goes, Tatsu staring, and after him (edo.vouched). Then the supper. */
async function vouch(g) {
  for (const id of THREE) { const a = g.actor(id); if (a && a.hold) a.hold(false); }
  const k = g.actor("kurata"), t = g.actor("tatsu");
  await Promise.all([k ? walkOf(g, "kurata", [M.kurataTo]) : null, t ? g.wait(400).then(() => walkOf(g, "tatsu", [M.tatsuTo])) : null]);
  look(g, "kurata", "natsu"); look(g, "tatsu", "mom"); look(g, "natsu", "kurata");
  for (const id of THREE) look(g, id, M.kurataTo);
  await g.say(VOUCH[1], VOUCH[2]);
  hold(g, "kurata", "riceball");                                                  // (he takes a rice ball from the tray, and looks at it)
  hold(g, "tatsu", "peer");
  await g.wait(900);
  await g.say(VOUCH[3]);
  // on he goes along the shore, the rice ball in his hand; Tatsu stares at the three of them, and follows him
  await Promise.all([k ? walkOff(g, "kurata", [[220, 540], [-30, 545]]) : null,
    t ? g.wait(700).then(() => { hold(g, "tatsu", null); return walkOff(g, "tatsu", [[240, 556], [-30, 560]]); }) : null]);
  await g.say(VOUCH[4], VOUCH[5]);
  g.flag("edo.vouched", true);
  await natsuTalk(g);
}

// ---------- #28: the people of the shore ----------
const RIHEI = riheiTree({});
const KYUHACHI = kyuhachiTree({});
async function riheiTalk(g) { faceLead(g, "rihei"); await g.talk(RIHEI); }
async function kyuhachiTalk(g) {
  faceLead(g, "kyuhachi");
  if (is(g, "edo.pickleServed") && !is(g, "edo.fifthCaught") && who(g) === "lilsis") return task("tub")(g);      // (he is at her tub: the fifth)
  hold(g, "kyuhachi", "lend");
  await g.talk(KYUHACHI);
  hold(g, "kyuhachi", null);
  if (is(g, "edo.pickleServed") && !is(g, "edo.fifthCaught")) hold(g, "kyuhachi", "ladleout");
}
/** Kurata and Tatsu, used: the family never answers the magistrate's men (their own words, by the lead). */
const kurataUse = (g) => g.say(mine(g, "edo.dojima.kurata.use"));
kurataUse.lines = THREE.map((w) => `edo.dojima.kurata.use.${w}`);
const tatsuUse = (g) => g.say(mine(g, "edo.dojima.tatsu.use"));
tatsuUse.lines = THREE.map((w) => `edo.dojima.tatsu.use.${w}`);
/** Little Sister by the water men: splashed ("I wasn't even SHOUTING."). The splash, and her own line; the others keep away. */
const watermenUse = Object.assign(async (g) => {
  if (who(g) === "lilsis") { await splash(g, true); }
  await g.say(mine(g, "edo.dojima.watermen.use"));
}, { lines: THREE.map((w) => `edo.dojima.watermen.use.${w}`) });

/** The rice market: Big Sister's look is two boxes (Mom: "Don't explain it, darling. Not on an empty stomach."). */
const marketLook = Object.assign((g) => g.say(...(who(g) === "bigsis" ? ["edo.dojima.market.bigsis", "edo.dojima.market.bigsis.2"] : [mine(g, "edo.dojima.market")])),
  { lines: [...THREE.map((w) => `edo.dojima.market.${w}`), "edo.dojima.market.bigsis.2"] });

// ---------- the way on, and the way back ----------
/** The right edge, into the town: not hungry yet, not without thanking her; then on, with O-Natsu gone ahead. */
async function townUse(g) {
  const me = who(g);
  if (!is(g, "edo.paddle")) return g.say(`edo.dojima.town.notyet.${me}`);
  if (!is(g, "edo.supped")) return g.say(`edo.dojima.town.thanks.${me}`);
  await g.goto("edo-street", { spawn: "shore" });
}
townUse.lines = THREE.flatMap((w) => [`edo.dojima.town.notyet.${w}`, `edo.dojima.town.thanks.${w}`]);

// ---------- now and then: a bucket thrown at the dealers; the runner with the price ----------
/** The nearer water man throws a bucket at the dealers who will not stop (PAINT-21C's five frames, half a second), and
    Rihei shakes himself. `at`: at Little Sister, who has come too close. */
async function splash(g, at = false) {
  const p = g.plane("splash");
  if (!p) return;
  if (at && g.lead) { p.place(g.lead.x - 40, g.lead.y - 60); } else p.place(559, 424);
  p.now = 0;
  p.show(true);
  g.sfx("splash");
  await g.wait(520);
  p.show(false);
  if (!at) fidget(g, "rihei", "shakewet");
}
const RUN = { from: [553, 464], to: [830, 545], speed: 150 };
function tick(g, dt) {
  if (!g.scene || g.scene.id !== "edo-dojima" || !g.life || !g.life.enabled) return;
  const r = shore.running, p = g.plane("runner");
  if (r && p) {                                                                   // the runner, sprinting off with the price
    r.t += dt / 1000;
    const len = Math.hypot(RUN.to[0] - RUN.from[0], RUN.to[1] - RUN.from[1]), u = Math.min(1, (r.t * RUN.speed) / len);
    const x = RUN.from[0] + (RUN.to[0] - RUN.from[0]) * u, y = RUN.from[1] + (RUN.to[1] - RUN.from[1]) * u;
    p.place(x, y, g.sizeAt(x, y) / g.sizeAt(RUN.from[0], RUN.from[1]));
    p.base = y;
    if (u >= 1) { p.show(false); shore.running = null; }
  }
  if (g.busy || g.dialogue.active) return;
  if ((shore.splashAt -= dt) <= 0) { shore.splashAt = 6000 + Math.random() * 6000; splash(g); }
  if (!shore.running && (shore.runAt -= dt) <= 0 && p) {
    shore.runAt = 26000 + Math.random() * 24000;
    shore.running = { t: 0 };
    p.show(true);
  }
}

// ---------- the scene ----------
const PEOPLE = ["natsu", "rihei", "kyuhachi", "kurata", "tatsu", "awafather", "awamother", "oldpilgrim", "ladleboy"];
const thing = (id, name, shape, walkTo, face, more = {}) => ({ id, name, ...shape, walkTo, face, ...lookUse("edo.dojima", id), ...more });
const inLine = (g) => !is(g, "edo.fedPilgrims");
/** The stall's things, where the one working there stands: behind the table at her task's mark while the line is served. */
const serving = (g) => is(g, "edo.paddle") && !is(g, "edo.fedPilgrims");

export default {
  id: "edo-dojima",
  era: "edo",
  name: "The Dōjima shore",
  music: "edo-city",                                                             // (ENGINE-21's track: quick, plucked, a crowd under it)

  // DEPTH (layout.json: an outdoor camera, horizon 262, full 590, the eye 3.59 m up): one floor, the shore street from the
  // bottom to O-Natsu's house front and the stone lip of the bank (the steps go down beyond it: nobody walks them)
  horizon: 262, full: 590,
  walk: { area: [[0, 596], [800, 596], [800, 470], [708, 466], [619, 461], [534, 457], [453, 453], [375, 449], [368, 456], [114, 443], [128, 437], [0, 431]] },
  // the stall's row (sandals to kettle), the bales by the door, the dealers and the water men, their spare buckets, the
  // bales at the front (layout.json blocked)
  blocked: [
    [[73, 472], [344, 489], [359, 473], [105, 459]], [[120, 441], [178, 444], [155, 455], [94, 451]], [[489, 465], [835, 483], [809, 462], [496, 447]],
    [[491, 475], [528, 477], [530, 467], [495, 465]], [[601, 623], [1012, 660], [934, 589], [596, 563]],
    [[-10, 424], [42, 425], [42, 610], [-10, 610]],
  ],

  party: THREE,
  // (the girls' own marks, their places on landing: where the engine puts them on a game loaded or started here with nobody
  // placed yet. No mark is named "mom": hers would be the landing's own point, and a lead standing on two marks is on her own,
  // so LEG_START.osaka would load on "mom", not on "landing"; started here with no mark, Mom is on `landing`, the default)
  spawn: { default: M.landing, ...M, landing_mom: LANDING_AT.mom, landing_bigsis: LANDING_AT.bigsis, landing_lilsis: LANDING_AT.lilsis,
    bigsis: LANDING_AT.bigsis, lilsis: LANDING_AT.lilsis },
  // up the river steps (the lighter's): whoever leads on `landing`, the other two beside her; back from the street at the right
  arrive: { landing: [LANDING_AT.bigsis, LANDING_AT.lilsis], town: [[760, 556], [770, 580]] },
  facing: "S",
  exits: ["edo-street"],
  edges: { E: { to: "edo-street", spawn: "shore", name: "into the town", use: townUse } },
  stock: STOCK_DRESSED,
  talk: talkFor({
    lilsis: { mom: [{ when: (g) => !is(g, "edo.paddle"), say: ["edo.dojima.talk.lilsis.mom.ladle.a", "edo.dojima.talk.lilsis.mom.ladle.b"] }] },
    bigsis: { mom: [{ when: (g) => is(g, "edo.paddle"), say: ["edo.dojima.talk.bigsis.mom.paddle.a", "edo.dojima.talk.bigsis.mom.paddle.b"] }] },
  }),
  tick,

  picture: art + "back.png",
  // CUT-OUTS, back to front (PAINT-21C's plan): the lighter moored off the steps (gone once it has left them), the market's
  // dealers and water men, O-Natsu's noren, and the stall on one base listed in order (the sandals, the pot on its hearth,
  // the table and its tub, the tray over the table, the kettle); the bales at the front; and the two moving pictures the
  // scene shows now and then (PAINT-21C's frames, not an engine kind): a bucket's splash, and the runner with the price.
  planes: [
    { id: "lighter", src: art + "lighter.png", base: [[356, 441], [603, 453]], when: (g) => !is(g, "edo.landed") },
    { id: "market", src: art + "market.png", base: [[489, 465], [834, 483]] },
    { id: "noren", src: art + "noren.png", base: [[175, 444], [252, 448]] },
    { id: "sandals", states: { full: art + "sandals.png", few: art + "sandals-few.png" }, state: (g) => (is(g, "edo.fedPilgrims") ? "few" : "full"), base: [[102, 473], [351, 488]] },
    { id: "pot", src: art + "pot.png", base: [[102, 473], [351, 488]] },
    { id: "stall", src: art + "stall.png", base: [[102, 473], [351, 488]] },
    { id: "tray", states: { full: art + "tray.png", half: art + "tray-half.png", empty: art + "tray-empty.png" },
      state: (g) => (is(g, "edo.fedPilgrims") ? "empty" : is(g, "edo.ballsShaped") ? "half" : "full"), base: [[102, 473], [351, 488]] },
    { id: "kettle", src: art + "kettle.png", base: [[102, 473], [351, 488]] },
    { id: "front", src: art + "front.png", plane: "front" },
    { id: "splash", frames: [1, 2, 3, 4, 5].map((n) => `${art}splash-${n}.png`), fps: 10, at: [559, 424], foot: [5, 26], base: [[489, 465], [835, 483]], when: () => false },
    { id: "runner", frames: [1, 2, 3, 4].map((n) => `${art}runner-${n}.png`), fps: 9, at: RUN.from, foot: [27, 75], base: 464, when: () => false },
    { id: "near", src: art + "near.png", plane: "front" },
  ],
  // THINGS THAT MOVE BY NATURE (layout.json fx): steam from the pot and the kettle, the hearth's embers, the noren stirring,
  // the moored lighter riding at the steps, the light moving on the river, and lighters poled past on it, both ways (painted
  // glide frames, clipped to the river between O-Natsu's house and the bridge)
  fx: [
    { id: "pot-steam", type: "smoke", at: [182, 425], base: [[102, 473], [351, 488]], height: 74, width: [5, 30], lean: [-22, -74], rise: 14, rate: 3.0, gust: 0.25, color: "#f2f0ea", opacity: 0.34 },
    { id: "kettle-steam", type: "smoke", at: [347, 446], base: [[102, 473], [351, 488]], height: 28, width: [1, 6], lean: [-8, -28], rise: 8, rate: 2.0, gust: 0.3, color: "#f2f0ea", opacity: 0.28 },
    { id: "hearth-embers", type: "embers", at: [171, 471], size: [5, 2], base: [[102, 473], [351, 488]], glowOpacity: 0.15, sparks: 0.1 },
    { id: "noren-sway", type: "sway", plane: "noren", anchor: "top", amount: 2.0, period: 3.6, wave: 24, lean: 0.3 },
    { id: "lighter-bob", type: "bob", plane: "lighter", amount: 1, period: 5.5, tilt: 0.8, when: (g) => !is(g, "edo.landed") },
    { id: "river-shimmer", type: "shimmer", plane: "back", poly: [[432, 300], [800, 300], [800, 462], [685, 457], [576, 452], [473, 447], [375, 442], [432, 440]],
      count: 26, size: 5, flow: [3, 0], life: 2.0, color: "#f6eed8", opacity: 0.42 },
    { id: "lighters-near", type: "birds", plane: "back", lanes: [[[-160, 382], [960, 423]]], every: [28, 56], group: [1, 1], speed: 12, size: 189,
      frames: { glide: [art + "lighter-near.png"], foot: [92, 65], face: "E", mirror: true }, clip: [[[432, 300], [702, 300], [702, 452], [432, 452]]] },
    { id: "lighters-far", type: "birds", plane: "back", lanes: [[[-160, 345], [960, 375]]], every: [22, 46], group: [1, 1], speed: 9, size: 116, seed: 5,
      frames: { glide: [art + "lighter-far.png"], foot: [58, 45], face: "E", mirror: true }, clip: [[[432, 300], [702, 300], [702, 452], [432, 452]]] },
  ],

  // The people of the shore (PEOPLE-21A's kinds, at the painter's marks): O-Natsu at her stall's right end (behind the kettle;
  // she lets the three past her to their places: not solid), the pilgrims in their line until it is fed, Kyūhachi, who has
  // been through it four times, Rihei among the dealers, and Kurata and Tatsu walking the shore until they come along it.
  actors: [
    { id: "natsu", kind: "natsu", at: M.natsu, face: "S", solid: false, when: (g) => !is(g, "edo.combAsked"), life: { fidget: [6, 12], still: true } },
    { id: "awafather", kind: "awafather", at: M.line1, face: "N", when: inLine, life: { fidget: [5, 11], still: true } },
    { id: "awamother", kind: "awamother", at: M.line2, face: "N", when: inLine, life: { fidget: [5, 11], still: true } },
    { id: "oldpilgrim", kind: "oldpilgrim", at: M.line3, face: "N", when: inLine, life: { fidget: [6, 12], still: true } },
    { id: "ladleboy", kind: "ladleboy", at: M.line4, face: "N", when: inLine, life: { fidget: [4, 9], still: true } },
    { id: "kyuhachi", kind: "kyuhachi", at: M.kyuhachi, face: "W", life: { fidget: [5, 10], still: true } },
    { id: "rihei", kind: "rihei", at: M.rihei, face: "S", life: { fidget: [4, 8], still: true } },
    { id: "kurata", kind: "kurata", at: KURATA_AT, face: "W", when: (g) => !is(g, "edo.vouched"),
      life: { fidget: [8, 14], every: [16, 30], spots: [[560, 512, "W"], [700, 532, "W"]], stay: [5, 10] } },
    { id: "tatsu", kind: "tatsu", at: TATSU_AT, face: "W", when: (g) => !is(g, "edo.vouched"),
      life: { fidget: [6, 12], every: [16, 30], spots: [[600, 530, "W"], [736, 552, "W"]], stay: [5, 10] } },
  ],

  // Back to front: a later area lies over an earlier one (the other two first: edo-hills.js MATES).
  hotspots: [
    ...MATES,
    thing("warehouses", "warehouses", { rect: [576, 192, 224, 150] }, M.landing, "N"),
    thing("castle", "castle", { rect: [418, 196, 186, 72] }, M.landing, "N"),
    thing("river", "river", { poly: [[432, 300], [800, 300], [800, 462], [685, 457], [576, 452], [473, 447], [375, 442], [432, 440]] }, M.landing, "N"),
    thing("lighters", "lighters", { rect: [440, 330, 250, 90] }, M.landing, "N"),
    thing("bridge", "bridge", { rect: [667, 254, 132, 215] }, [700, 530], "NE"),
    thing("steps", "river steps", { poly: [[429, 452], [544, 458], [550, 422], [460, 419]] }, M.landing, "N"),
    thing("house", "rice dealer's house", { poly: [[121, 441], [362, 454], [434, 388], [434, 223], [429, 145], [198, 152], [83, 210]] }, [160, 500], "N"),
    thing("noren", "noren", { rect: [174, 337, 79, 50] }, [160, 500], "N"),
    // the market: the dealers (hands up) and the water men (their buckets) are PAINT-21C's two shapes over the crowd; the market
    // itself is the road at their feet, where it spills into the street (so that all three can be clicked); the runner's lane
    thing("dealers", "dealers", { rect: [572, 361, 225, 104] }, [660, 512], "N"),
    thing("watermen", "water men", { rect: [512, 367, 60, 98] }, M.watermen, "N", { use: watermenUse }),
    thing("market", "rice market", { poly: [[489, 462], [800, 474], [800, 494], [489, 482]] }, [640, 510], "N", { look: marketLook }),
    thing("runner", "runner", { rect: [600, 488, 110, 26] }, [640, 530], "E"),
    thing("bucket", "bucket", { rect: [489, 446, 54, 34] }, M.watermen, "W"),
    // the stall and its things (before the paddle, looked at and tried from the front; while the line is served, the one
    // working at it goes behind the table to her place)
    thing("stall", "alms stall", { rect: [79, 412, 270, 73] }, [168, 500], "N", { use: stallUse }),
    thing("sandals", "straw sandals", { rect: [76, 452, 83, 26] }, [150, 500], "N"),
    thing("pot", "rice pot", { rect: [144, 418, 74, 66] }, [176, 500], "N", { use: task("pot"), when: (g) => !serving(g) }),
    thing("tray", "rice balls", { rect: [209, 420, 64, 19] }, [176, 500], "N", { use: task("tray"), when: (g) => !serving(g) }),
    thing("tub", "pickled radish", { rect: [276, 409, 30, 30] }, [330, 502], "N", { use: task("tub"), when: (g) => !serving(g) }),
    { ...thing("pot", "rice pot", { rect: [144, 418, 74, 66] }, M.pot, "S"), id: "pot-serve", use: task("pot"), verb: "Serve from", when: serving },
    { ...thing("tray", "rice balls", { rect: [209, 420, 64, 19] }, M.balls, "S"), id: "tray-serve", use: task("tray"), verb: "Shape", when: serving },
    { ...thing("tub", "pickled radish", { rect: [276, 409, 30, 30] }, M.pickle, "S"), id: "tub-serve", use: task("tub"), verb: "Hand out", when: serving },
    thing("kettle", "kettle", { rect: [297, 436, 55, 52] }, [330, 502], "N"),
    // the people (the game draws them; their areas go with them)
    { id: "natsu", name: "O-Natsu", verb: "Talk to", rect: [336, 382, 28, 82], walkTo: [330, 500], face: "N", look: each("edo.dojima.natsu"), use: natsuTalk,
      useWith: { paddle: natsuTalk }, when: (g) => !is(g, "edo.combAsked") },
    { id: "awafather", name: "pilgrim", verb: "Talk to", rect: [198, 393, 34, 100], walkTo: [176, 510], face: "E", look: each("edo.dojima.awafather"),
      use: nth("edo.dojima.awafather", "awafather"), when: inLine },
    { id: "awamother", name: "pilgrim with a baby", verb: "Talk to", rect: [218, 411, 35, 102], walkTo: [196, 532], face: "E", look: each("edo.dojima.awamother"),
      use: nth("edo.dojima.awamother", "awamother"), when: inLine },
    { id: "oldpilgrim", name: "old pilgrim", verb: "Talk to", rect: [241, 423, 39, 115], walkTo: [222, 560], face: "E", look: each("edo.dojima.oldpilgrim"),
      use: nth("edo.dojima.oldpilgrim", "oldpilgrim"), when: inLine },
    { id: "ladleboy", name: "boy with a ladle", verb: "Talk to", rect: [284, 476, 32, 94], walkTo: [262, 584], face: "E", look: each("edo.dojima.ladleboy"),
      use: nth("edo.dojima.ladleboy", "ladleboy"), when: inLine },
    { id: "kyuhachi", name: "Kyūhachi", verb: "Talk to", rect: [368, 430, 44, 130], walkTo: [356, 572], face: "E", look: each("edo.dojima.kyuhachi"), use: kyuhachiTalk },
    { id: "rihei", name: "Rihei", verb: "Talk to", rect: [687, 385, 32, 95], walkTo: [680, 512], face: "N", look: each("edo.dojima.rihei"), use: riheiTalk },
    { id: "kurata", name: "the official", rect: [610, 410, 32, 114], walkTo: [600, 560], face: "E", look: each("edo.dojima.kurata"), use: kurataUse,
      when: (g) => !is(g, "edo.vouched") },
    { id: "tatsu", name: "the staring man", rect: [652, 430, 32, 112], walkTo: [610, 572], face: "E", look: each("edo.dojima.tatsu"), use: tatsuUse,
      when: (g) => !is(g, "edo.vouched") },
    // the way into the town, at the right edge (and its band: edges.E)
    { id: "town", name: "the way into town", verb: "Go", rect: [756, 470, 44, 126], walkTo: M.town, face: "E", look: each("edo.dojima.town"), use: townUse },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and whenever the scene is built.
  setup(g) {
    shore.splashAt = 8000; shore.runAt = 18000; shore.running = null;
    dressFor(g, "outdoors");
    for (const id of THREE) { const now = g.dressOf(id); if (now && now.endsWith("-step")) g.dress(id, now.replace(/-step$/, "")); }      // (a save caught at supper: up again)
    g.loop("crowd", { level: 0.5 });
    // Kyūhachi at Little Sister's tub, his fifth time round, if a save caught him there
    if (is(g, "edo.pickleServed") && !is(g, "edo.fifthCaught")) {
      const k = g.actor("kyuhachi");
      if (k) { k.place(FIFTH_AT[0], FIFTH_AT[1], g.sizeAt(FIFTH_AT[0], FIFTH_AT[1])); k.face("N"); if (k.hold) k.hold(true, "ladleout"); }
    }
  },

  // The landing (the first time: the lighter's last); and a game saved between the line fed and the supper goes on to the
  // supper (the tree's own start reads the facts).
  async enter(g) {
    if (!is(g, "edo.landed")) return landing(g);
    if (is(g, "edo.fedPilgrims") && !is(g, "edo.vouched")) return vouch(g);
  },
};

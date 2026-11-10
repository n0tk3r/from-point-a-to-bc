// Act Six, the third leg: the castle approach at Himeji, late afternoon (SCENES-20C: new in round twenty, in place of
// ENGINE-20's sketch; briefs/SCENES-20.md, and the design, briefs/out/edo-design.md, "edo-castle" and #28). In the
// foreground the one old double cherry in full late bloom, its petals drifting; the stone ramp up to the Ni-no-mon gate
// tower (the cross-marked tile on its gable, small, for whoever looks); two gate guards in the opening; plasterers'
// scaffolding on the white wall, a tub of lime and three buckets; beyond, the keep, white on its stone base; herons in the
// moat, every one facing the top of the keep. Now and then Himeji people pass on the road below, ladles in hand, going east.
//
// The three of them come here by the road ("Three days later", js/content/cutscenes/edo-walk.js: SCENES-20B's), at the
// mark `enter`. The leg's start is LEG_START.himeji (edo-common.js).
// SCENES-21C (round twenty-one): they come here the next day now, from Himeji town (the end of "Mind The Fire",
// js/content/cutscenes/edo-night.js: edo.nightDone), at the same mark `enter`, the road from the town; and the road back into
// the town is a way out at the left edge (edo-town, at its gate), as the town's lane north is the way here. By the map,
// Shosha has done its part (SHOSHA_MAP.done).
//
//   #28 Eight At The Gate   Tomezō, up his ladder, cannot hear anyone over himself: Little Sister hollers him down
//                           (tomezoTree, js/content/talk/edo-b.js). His own trowel back, and Jinsuke's name: he asks nothing
//                           more. Three hands short, and three here: the plasterers' white head-cloths (`edo-crew`), a
//                           bucket each. The guards count everyone in and out (guardTree): before the crew, "Name. House.
//                           Business."; with it, eight went out and eight come in, and the eight go up the ramp and through
//                           the gate, counted, the three of them last with their buckets (edo.inside): edo-keep.
//   the cross               from the mark `tile`, the gable's round end tile: a cross on it. The first time Big Sister looks,
//                           "Nobody knows who put it there." "Somebody did." (edo.castle.gable.found.1, .2)
//   the cherry              everyone has a line; Little Sister lies under it, and the petals land on her face (`edo-lying`).
//
// The trees are WRITE-20B's, with three changes of staging made here (not in the talk file; ready.md lists them): the
// trowel goes into Tomezō's hand as it is offered, before his lines; the head-cloths go on after his "Head-cloths, white,
// like mine", before Little Sister's "I'm a plasterer now"; and the count is said while the eight walk through the gate.
//
// Every place is the painter's own measurement of the finished picture (art/scenes/edo-castle/layout.json, PAINT-20D's
// ready.md), or was set by eye against the picture with the people in it; where the two differ the comment says why.
//
// Try it: index.html?scene=edo-castle&lead=mom&flags=edo.nightDone   (and LEG_START.himeji's pockets and clothes, which a
// jump does not give: the play sets them up as the leg begins)      (SCENES-21C: edo.nightDone, was edo.walked)

import { STOCK_DRESSED } from "./edo-common.js";
import { THREE, who, is, heard, each, holderOf, idle, chatter, swap, dressAll, TALK } from "./edo-himeji.js";
import { tomezoTree, guardTree } from "../talk/edo-b.js";
import { SHOSHA_MAP } from "../talk/edo-d.js";      // SCENES-21C: Shosha refused by the map, the next day
import { scaleAt } from "../../engine/walk.js";

const art = "art/scenes/edo-castle/";

// ---------- the camera and the ground (layout.json: the land camera, horizon 290, full 588) ----------
const HORIZON = 290, FULL = 588;
const FLOOR = [[6, 596], [794, 596], [794, 544], [584, 542], [604, 472], [784, 466], [784, 442], [725, 442], [725, 422], [633, 422], [633, 442], [453, 442], [453, 464], [450, 472], [430, 542], [418, 534], [430, 492], [300, 494], [120, 492], [6, 490]];
const sizeAt = (y) => Math.max(0.3, (y - HORIZON) / (FULL - HORIZON));

// ---------- the marks (layout.json marks and faces) ----------
const M = { enter: [150, 580], cherry: [176, 526], ladder: [586, 468], crew: [494, 466], gate: [679, 444], guard1: [642, 448], guard2: [716, 448],
  tile: [560, 520], moat: [300, 506], road: [420, 584], underBoughs: [228, 512], toKeep: [679, 426] };
const PILGRIMS = { from: [812, 574], via: [[700, 578], [560, 586], [400, 590], [240, 586], [100, 590]], to: [-14, 590] };
// Tomezō up his ladder: his place is the ground under his feet (the ladder's foot row, 464), and the rig draws him 137 cm up,
// on rung 6 (PEOPLE-20's tomezo-ladder, LADDER_RUNG), in front of the gate (whose base is 436). His feet are on row 391 there
// (marks.tomezo [604, 392]: layout.json ladder.rung_rows[5]); coming down he is drawn at the ladder's depth all the way.
const LADDER_FOOT = [604, 464], RUNG6 = [606, 392], LADDER_SCALE = 0.584, LADDER_BASE = 465;
const TOMEZO_DOWN = [624, 470];        // down off the ladder: a step to its right, turned to whoever hollered (the terrace's front)
const TALK_TOMEZO = [588, 470];        // where the one talking to him stands, down: the ladder's foot (marks.ladder), a pace on
const AT_GUARDS = [679, 462];          // before the gate, between the two guards, a pace in front of them
// The crew of five (Tomezō and four): two on the scaffold's lifts (stands scaffold1, scaffold2: the scaffold's depth, base 451;
// 0.54 of full size by the painter's "a 1.56 m man is 75 px"), one at the tub with the mixing pole, one by the scaffold's end.
const LIFT1 = [486, 404], LIFT2 = [536, 372], LIFT_SCALE = 0.54, LIFT_BASE = 451;
// (Clear of the lifts: a man on the ground under a lift would stand in front of the legs of the man on it.)
const MIXER = [550, 463], P2 = [512, 444];
// The three buckets of lime (layout.json things.buckets.each: their stands), one each, picked up as the eight go in.
const BUCKETS = { mom: { id: "bucket-1", at: [500, 512] }, bigsis: { id: "bucket-2", at: [527, 521] }, lilsis: { id: "bucket-3", at: [553, 508] } };
// The way through: up onto the terrace, into the opening between the guards, and on into the passage (behind gate.png's base).
const THROUGH = [[679, 448], [679, 430], [679, 423]];

// ---------- the story ----------
const crewOut = (g) => !is(g, "edo.inside");
const down = (g) => is(g, "edo.tomezoDown");
const crew = (g) => is(g, "edo.crew");
const outfit = (g) => (crew(g) ? "edo-crew" : "edo");

// ---------- #28: Tomezō ----------
/** The hook `down`: he climbs down his ladder (after Little Sister's holler): from rung 6 to its foot, at the ladder's depth
    all the way and in front of the gate, his back to us; then a step to the right and round to her. */
async function tomezoDown(g) {
  const lil = g.actor("lilsis");
  if (lil && lil.act && lil.act.low === "holler") lil.hold(false);
  const f = swap(g, "tomezo", "tomezo", RUNG6, "N", LADDER_SCALE, LADDER_BASE);
  await g.view.cast.load();
  if (!g.clock.skipping) {
    f.walking = true;
    try { await g.tween(1500, (k) => { f.place(RUNG6[0] + (LADDER_FOOT[0] - RUNG6[0]) * k, RUNG6[1] + (LADDER_FOOT[1] - RUNG6[1]) * k, LADDER_SCALE); f.phase = (k * 3) % 1; }); }
    finally { f.walking = false; }
  }
  f.place(LADDER_FOOT[0], LADDER_FOOT[1], sizeAt(LADDER_FOOT[1]));
  f.base = null;
  await f.walkPath(g.clock, [TOMEZO_DOWN], sizeAt);
  const lead = g.lead;
  if (lead) { f.look(lead.x, lead.y); lead.look(f.x, f.y); }
}
/** The hook `trowel` (staged here: the tree's lines for it are said after the trowel is in his hand): she holds it out, he
    takes it. Whoever has it in the talk gives it. */
const TROWEL_LINES = [];
async function takeTrowel(g) {
  const lead = g.lead, t = g.actor("tomezo");
  if (lead && t) lead.look(t.x, t.y);
  await g.reach();
  g.take("trowel");
  g.sfx("pickup");
  if (t && t.fidget) t.fidget("wipebrow");
  await g.say(...TROWEL_LINES);
}
/** The hook `dress` (staged here: after his "Head-cloths, white, like mine. Bucket each.", before Little Sister's "I'm a
    plasterer now"): the three of them in the plasterers' white head-cloths, one after another. */
const HANDS_AFTER = [];
async function dressCrew(g) {
  for (const id of ["mom", "bigsis", "lilsis"]) {
    const a = g.actor(id);
    if (a && a.play) await a.play(g.clock, "reach");
    g.dress(id, "edo-crew");
    g.sfx("noren");                                                          // (cloth)
    await g.wait(160);
  }
  await g.say(...HANDS_AFTER);
}
const TOMEZO = (() => {
  const t = tomezoTree({ down: tomezoDown, trowel: takeTrowel, dress: dressCrew });
  // the trowel: its lines into the hook, said after it has changed hands
  const o = t.nodes.down.options.find((x) => x.id === "trowel");
  TROWEL_LINES.push(...o.say); delete o.say;
  // the head-cloths: after his second line, before hers
  HANDS_AFTER.push(...t.nodes.hands.say.slice(2)); t.nodes.hands.say = t.nodes.hands.say.slice(0, 2);
  return t;
})();
/** A word with Tomezō: up the ladder, Little Sister has her hands cupped round her mouth before she hollers (her one way
    to be heard); down, he is turned to whoever is talking. */
async function tomezoUse(g) {
  const lil = g.actor("lilsis"), t = g.actor("tomezo"), hollering = !down(g) && who(g) === "lilsis";
  if (down(g) && t && g.lead) { t.look(g.lead.x, g.lead.y); g.lead.look(t.x, t.y); }
  if (hollering && lil) lil.hold(true, "holler");
  try { await g.talk(TOMEZO); }
  finally { if (lil && lil.act && lil.act.low === "holler") lil.hold(false); }
}

// ---------- #28: the guards, and the count ----------
const COUNT_LINES = [];
/** Someone walks (by the walk map, round things) to a point, if they are on the stage. */
const walkTo = (g, id, at) => (g.actor(id) ? g.walkTo(at[0], at[1], id) : Promise.resolve());
/** Someone goes through the gate: up into the opening, past the guards, into the passage, and out of sight. */
async function through(g, id, delay = 0) {
  const a = g.actor(id);
  if (!a) return;
  if (delay) await g.wait(delay);
  await a.walkPath(g.clock, THROUGH, sizeAt);
  await g.tween(300, (k) => a.fade(1 - k));
  a.hidden = true;
}
/** The hook `count` (guardTree, with the crew: the tree sets edo.inside first; its lines are said here, as the eight go
    through). Tomezō to the gate and his word; the three take up a bucket each; the four plasterers come down and go in,
    and Tomezō, counted one to five; Mom and Big Sister, six and seven; Little Sister last, at the threshold: eight. Then
    through, and into the keep. */
async function count(g) {
  const [say1, five, sixSeven, eight, ...rest] = COUNT_LINES;
  const g1 = g.actor("guard1"), g2 = g.actor("guard2");
  // the crew gathers: off the scaffold, from the tub and the scaffold's end, to the foot of the terrace
  const lift = async (id, from) => {
    const a = g.actor(id);
    if (!a) return;
    const foot = [from[0], LIFT_BASE + 4];
    if (a.act) a.hold(false);
    if (!g.clock.skipping) { a.walking = true; try { await g.tween(900, (k) => { a.place(from[0], from[1] + (foot[1] - from[1]) * k, LIFT_SCALE + (sizeAt(foot[1]) - LIFT_SCALE) * k); a.phase = (k * 2) % 1; }); } finally { a.walking = false; } }
    a.place(foot[0], foot[1], sizeAt(foot[1])); a.base = null;
  };
  const p1 = g.actor("plasterer1");
  if (p1 && p1.act) p1.hold(false);
  await Promise.all([
    walkTo(g, "tomezo", [640, 458]).then(() => { const t = g.actor("tomezo"); if (t) t.face("N"); }),
    lift("plasterer3", LIFT1), lift("plasterer4", LIFT2),
    // the three, a bucket each: down to it, up with it (the bucket goes from the ground: she carries it)
    ...THREE.map((id) => walkTo(g, id, BUCKETS[id].at).then(async () => { const a = g.actor(id); if (a && a.play) { a.face("N"); await a.play(g.clock, "pick"); } const b = g.plane(BUCKETS[id].id); if (b) b.show(false); })),
  ]);
  g.sfx("lime");
  if (!heard(g, "edo.castle.plasterer.2") && g.actor("plasterer2")) await g.say("edo.castle.plasterer.2");      // (to the tall one, as she lifts hers)
  await g.say(say1);
  // one to five: the crew go in, Tomezō last of them
  if (g1 && g1.fidget) g1.fidget("tally2");
  const crewIn = Promise.all(["plasterer1", "plasterer2", "plasterer3", "plasterer4", "tomezo"].map((id, n) => through(g, id, 300 + n * 520)));
  await g.wait(600);
  await g.say(five);
  await crewIn;
  // six, seven: Mom and Big Sister, up the ramp with their buckets
  if (g2 && g2.fidget) g2.fidget("tally2");
  const pair = Promise.all([["mom", 0], ["bigsis", 520]].map(async ([id, d]) => { await g.wait(d); await walkTo(g, id, [668, 470]); await through(g, id); }));
  await g.wait(900);
  await g.say(sixSeven);
  await pair;
  // eight: Little Sister, last, at the threshold
  await walkTo(g, "lilsis", [679, 458]);
  const lil = g.actor("lilsis");
  if (lil) await lil.walkPath(g.clock, [THROUGH[0]], sizeAt);
  if (g1 && g1.fidget) g1.fidget("tally2");
  await g.say(eight, ...rest);
  await through(g, "lilsis");
  await g.wait(250);
  await g.goto("edo-keep", { spawn: "enter" });
}
const GUARDS = (() => {
  const t = guardTree({ count });
  COUNT_LINES.push(...t.nodes.count.say);
  t.nodes.count.say = [];
  return t;
})();
async function guardsUse(g) {
  const lead = g.lead;
  if (lead) lead.face("N");
  await g.talk(GUARDS);
}
/** The gate itself: before the crew, its refusals (the guards ask); with the crew, the count. */
const gateUse = (g) => (crew(g) ? guardsUse(g) : g.say(`edo.castle.gate.use.${who(g)}`));

// ---------- the cross on the tile ----------
/** The gable, from the mark `tile`. The first time Big Sister looks, she finds it, and Mom has the last word. */
async function gableLook(g) {
  if (who(g) === "bigsis" && !heard(g, "edo.castle.gable.found.1")) return g.say("edo.castle.gable.found.1", "edo.castle.gable.found.2");
  return g.say(`edo.castle.gable.${who(g)}`);
}

// ---------- the cherry: Little Sister lies under it ----------
async function cherryUse(g) {
  if (who(g) !== "lilsis") return g.say(`edo.castle.cherry.use.${who(g)}`);
  const lil = g.lead, wear = outfit(g);
  await g.walkTo(M.underBoughs[0], M.underBoughs[1]);
  lil.face("E");                                                              // (lying: her head to the west, under the boughs)
  g.dress("lilsis", "edo-lying");
  try {
    await g.wait(700);
    await g.say("edo.castle.cherry.use.lilsis");
    await g.wait(300);
  } finally { g.dress("lilsis", wear); }
}

// ---------- the buckets ----------
const bucketsLook = (g) => g.say(crew(g) ? `edo.castle.buckets.crew.${who(g)}` : `edo.castle.buckets.${who(g)}`);
const bucketsUse = (g) => g.say(crew(g) ? `edo.castle.buckets.crew.${who(g)}` : `edo.castle.buckets.use.${who(g)}`);

// ---------- the plasterers at work, the pilgrims on the road, and what is said now and then ----------
// The crew work while the player watches: the two on the lifts trowel the wall, the one at the tub mixes (holds of their
// own: PEOPLE-20's trowelwall and mix, and the movements trowelling and mixing now and then), and the one behind the scaffold
// trowels the wall too. Not while a line is up.
const work = { next: {} };
const WORKERS = [["plasterer3", "trowelwall", "trowelling", 3200], ["plasterer4", "trowelwall", "trowelling", 4100], ["plasterer2", "trowelwall", "trowelling", 4700], ["plasterer1", "mix", "mixing", 3700]];
function workTick(g, dt) {
  if (!g.life || !g.life.enabled || g.dialogue.active || g.busy) return;
  for (const [id, hold, move, every] of WORKERS) {
    const a = g.actor(id);
    if (!a || a.hidden || a.walking) continue;
    work.next[id] = (work.next[id] ?? every) - dt;
    if (work.next[id] > 0) continue;
    work.next[id] = every + ((id.charCodeAt(9) * 37) % 1700);
    if (a.act && a.act.low === hold) a.hold(false);
    a.fidget(move).then(() => { if (g.actor(id) === a && !a.act && !a.walking && !a.hidden && crewOut(g)) a.hold(true, hold); });
  }
}
// The pilgrims: one at a time, every half a minute or so, from the right along the road below and off to the left (east),
// a ladle held up; each says a word as they pass the middle of the road. Never while one of the three stands on the near
// road (they would walk through her), nor while the people's own lives are off (the tests' ?still).
const road = { walker: null, next: 9000, n: 0 };
function pilgrimTick(g, dt) {
  if (!g.life || !g.life.enabled || !g.scene || g.scene.id !== "edo-castle" || road.walker) return;
  if ((road.next -= dt) > 0) return;
  if (!idle(g) || THREE.some((id) => { const a = g.actor(id); return a && !a.hidden && a.y > 566; })) { road.next = 2500; return; }
  road.next = 24000 + (road.n % 3) * 7000;
  const n = (road.n++ % 3) + 1, id = `pilgrim${n}`;
  const f = g.view.cast.addFigure(id, id, PILGRIMS.from[0], PILGRIMS.from[1], sizeAt(PILGRIMS.from[1])).face("W");
  road.walker = f;
  let spoke = false;
  const stopTalk = g.clock.every(() => {
    if (spoke || g.view.cast.get(id) !== f) { stopTalk(); return; }        // (said, or gone from the stage: the watch ends)
    if (f.x < 520 && idle(g)) { spoke = true; f.hold(true, "ladleout"); g.run(() => g.say(`edo.castle.pilgrim.${n}`), { settle: false }).then(() => { if (f.act) f.hold(false); }); }
  });
  f.walkPath(g.clock, [...PILGRIMS.via, PILGRIMS.to], sizeAt).then(() => { stopTalk(); if (g.view.cast.get(id) === f) g.view.cast.remove(id); if (road.walker === f) road.walker = null; });
}
// Now and then: Tomezō shouting at nobody, up his ladder; and one of the crew, grumbling about Ise.
const CHAT = chatter([
  { when: (g) => !down(g), say: ["edo.castle.tomezo.shout.1"] },
  { when: (g) => crewOut(g) && !!g.actor("plasterer1") && (!down(g) || !heard(g, "edo.castle.plasterer.1")), say: ["edo.castle.plasterer.1"] },      // (once Tomezo is down, not again)
  { when: (g) => !down(g), say: ["edo.castle.tomezo.shout.2"] },
], { first: [8, 12], every: [30, 46] });

// ---------- the scene ----------
/** A thing of the castle approach, by its painted shape (layout.json things), with a look and a use for each of the three. */
const thing = (id, name, shape, walkTo, face, more = {}) => ({ id, name, ...shape, walkTo, face, look: each(`edo.castle.${id}`), use: each(`edo.castle.${id}.use`), ...more });
const poly = (p) => ({ poly: p });

export default {
  id: "edo-castle",
  era: "edo",
  name: "The castle at Himeji",

  horizon: HORIZON, full: FULL, minScale: 0.3,
  walk: { area: FLOOR },
  // the tub's ground (its cut-out is solid too), and the scaffold's three front poles (layout.json planes.scaffold.solid)
  blocked: [[[496, 467], [544, 467], [542, 456], [498, 456]], [[459, 452], [465, 452], [465, 447], [459, 447]], [[507, 452], [513, 452], [513, 447], [507, 447]],
    [[555, 452], [561, 452], [561, 447], [555, 447]]],

  party: THREE,
  // They come up the road from the east (the walk): whoever leads on `enter`, the other two beside her.
  spawn: { default: M.enter, ...M },
  arrive: { enter: [[206, 586], [96, 588]] },
  facing: "E",
  stock: STOCK_DRESSED,
  talk: TALK,
  // SCENES-21C: the road back into the town (its gate), at the left edge; and by the map, Shosha has done its part
  edges: { W: { to: "edo-town", spawn: "gate", name: "back into the town", walkTo: [10, 586] } },
  exits: ["edo-town"],
  travel: (g) => (g.flag("edo.nightDone") ? SHOSHA_MAP.done : true),
  tick(g, dt) { workTick(g, dt); pilgrimTick(g, dt); CHAT.tick(g, dt); },

  picture: art + "back.png",
  // CUT-OUTS, back to front (the painter's plan): the ladder on the gate's wall (behind everybody), the gate (its opening
  // clear: whoever passes the threshold is drawn into the passage), the scaffold, the tub, the three buckets (each picked up
  // as the eight go in: the backdrop is complete under them), and the cherry (people on the bank are under its boughs).
  planes: [
    // (the painter put the ladder on the back plane; but it leans on the gate tower's wall, which is the gate's cut-out, so on
    // the back plane the wall covered it: it sorts a hair in front of the gate instead, and everyone on the terrace before it)
    { id: "ladder", src: art + "ladder.png", base: 437 },
    { id: "gate", src: art + "gate.png", base: 436, solid: [[575, 438], [627, 438], [627, 406], [575, 406]] },
    { id: "scaffold", src: art + "scaffold.png", base: 450 },
    { id: "tub", src: art + "tub.png", base: 466, solid: [[497, 467], [543, 467], [541, 457], [499, 457]] },
    { id: "bucket-1", src: art + "bucket-1.png", base: 494, solid: [[490, 495], [510, 495], [509, 488], [491, 488]], when: crewOut },
    { id: "bucket-2", src: art + "bucket-2.png", base: 503, solid: [[517, 504], [537, 504], [536, 497], [518, 497]], when: crewOut },
    { id: "bucket-3", src: art + "bucket-3.png", base: 490, solid: [[543, 491], [563, 491], [562, 484], [544, 484]], when: crewOut },
    { id: "cherry", src: art + "cherry.png", base: 548, solid: [[70, 550], [108, 550], [108, 538], [70, 538]] },
    // DEPTH-23 (round twenty-three, tools/paint/DEPTH.md): the near plane, in front of everybody: the old cherry's great limb
    // up the left edge and its boughs of blossom across the top-left, a pine's bough tips at the top right, the moat's stone
    // edge and its reeds along the bottom (edo_castle_near.py)
    { id: "near", src: art + "near.png", plane: "front" },
  ],

  // THINGS THAT MOVE BY NATURE (layout.json fx, in ENGINE-20's names): the double cherry's petals drifting down to the bank and
  // the road, a little to the left, in front of everybody under the tree; the herons and the egrets in the moat, every one
  // facing the keep (they never turn away, nor fly); a few glints on the still water.
  fx: [
    { id: "petals", type: "petals", from: [[10, 70], [270, 70], [290, 300], [260, 440], [120, 440], [0, 340]], floor: [[0, 560], [330, 546]],
      rate: 0.9, wind: -10, fall: 18, size: [2.5, 4], color: "#eeaac0", color2: "#f8d5de", settle: 2.6, opacity: 0.92, plane: "front" },
    { id: "herons", type: "birds", area: [[60, 450], [330, 448], [330, 476], [60, 478]], count: 3,
      frames: { foot: [48, 98], face: "E", sizeAt: 590, stand: ["heron-1.png", "heron-2.png"], look: ["heron-3.png", "heron-4.png"], walk: ["heron-5.png", "heron-6.png", "heron-7.png", "heron-8.png"], peck: ["heron-9.png", "heron-10.png"], turn: ["heron-11.png"] },
      shy: 0, fly: false, turn: false, depth: true, moves: { stand: 5, look: 3, peck: 1, walk: 1, turn: 0 }, walk: 5, plane: "back" },
    { id: "egrets", type: "birds", area: [[200, 452], [424, 448], [424, 472], [200, 474]], count: 2, seed: 3,
      frames: { foot: [48, 98], face: "E", sizeAt: 590, stand: ["egret-1.png", "egret-2.png"], look: ["egret-3.png", "egret-4.png"], walk: ["egret-5.png", "egret-6.png", "egret-7.png", "egret-8.png"], peck: ["egret-9.png", "egret-10.png"], turn: ["egret-11.png"] },
      shy: 0, fly: false, turn: false, depth: true, moves: { stand: 5, look: 3, peck: 1, walk: 1, turn: 0 }, walk: 5, plane: "back" },
    { id: "moat-light", type: "shimmer", poly: [[0, 442], [442, 442], [450, 482], [0, 484]], count: 5, size: 3, flow: [-1.5, 0], life: 2.4, color: "#f4fbff", opacity: 0.28, plane: "back" },
  ],

  // The people: Tomezō up his ladder (then down at its foot), the two guards in the opening, and his crew of four. Their
  // small lives are their own (PEOPLE-20): the guards stand stiff and count, Tomezō waves his trowel at nobody; the crew work
  // (workTick, above). Nobody but the guards moves from his mark by himself: they are at work.
  actors: [
    { id: "tomezo", kind: "tomezo-ladder", at: LADDER_FOOT, face: "N", when: (g) => !down(g), life: { fidget: [4, 8], still: true } },
    { id: "tomezo", kind: "tomezo", at: TOMEZO_DOWN, face: "W", when: (g) => down(g) && crewOut(g), life: { fidget: [6, 12], still: true } },
    { id: "guard1", kind: "guard1", at: M.guard1, face: "E", life: { fidget: [7, 13], still: true } },
    { id: "guard2", kind: "guard2", at: M.guard2, face: "W", life: { fidget: [7, 13], still: true } },
    { id: "plasterer1", kind: "plasterer1", at: MIXER, face: "W", when: crewOut, life: { fidget: false } },
    { id: "plasterer2", kind: "plasterer2", at: P2, face: "N", when: crewOut, life: { fidget: false } },
    { id: "plasterer3", kind: "plasterer2", at: LIFT1, scale: LIFT_SCALE, face: "N", when: crewOut, solid: false, life: { fidget: false } },
    { id: "plasterer4", kind: "plasterer2", at: LIFT2, scale: LIFT_SCALE, face: "N", when: crewOut, solid: false, life: { fidget: false } },
  ],

  // Back to front: a later area lies over an earlier one (layout.json things, their shapes and stands).
  hotspots: [
    thing("sky", "sky", poly([[0, 0], [800, 0], [800, 230], [470, 230], [470, 36], [250, 36], [250, 0]]), M.tile, "N"),
    thing("hills", "hills", poly([[430, 240], [800, 236], [800, 300], [430, 300]]), M.tile, "N"),
    // DEPTH-23: the keep staged again through the same camera (100 m off, turned forty degrees, its corridor turret on behind
    // the gate tower; its top ridge's middle where it was, x 360, row 34, for the herons): these two shapes measured again
    // (edo_castle_layout.py, from the painting)
    thing("keep", "the keep", poly([[281, 59], [273, 172], [228, 192], [255, 226], [206, 248], [236, 256], [213, 347], [594, 347], [594, 270], [483, 267], [513, 247], [463, 226], [491, 192], [446, 174], [439, 59], [341, 14]]), M.tile, "N"),
    thing("stonebase", "the keep's stone base", poly([[214, 345], [231, 291], [489, 291], [506, 345], [506, 346], [214, 346]]), M.tile, "N"),
    thing("wall", "white wall", poly([[0, 344], [574, 348], [574, 400], [0, 404]]), M.moat, "N"),
    thing("terrace", "terrace", poly([[445, 436], [800, 436], [800, 476], [606, 470], [448, 470], [445, 468]]), M.crew, "N"),
    thing("ramp", "stone ramp", poly([[422, 540], [592, 540], [612, 470], [442, 470]]), M.tile, "N"),
    thing("road", "road", poly([[0, 540], [432, 540], [582, 540], [800, 542], [800, 598], [0, 598]]), M.road, "N"),
    thing("moat", "moat", poly([[0, 438], [444, 438], [450, 484], [0, 486]]), M.moat, "N"),
    thing("herons", "herons", poly([[40, 440], [420, 440], [420, 484], [40, 484]]), M.moat, "N"),
    thing("gate", "gate", poly([[562, 300], [562, 297], [565, 221], [624, 177], [726, 177], [784, 221], [785, 222], [788, 297], [788, 300], [776, 438], [574, 438]]), AT_GUARDS, "N",
      { plane: "gate", use: gateUse, verb: "Go through" }),
    { id: "gable", name: "gable", poly: [[646, 227], [704, 227], [675, 188]], walkTo: M.tile, face: "N", look: gableLook, use: each("edo.castle.gable.use") },
    thing("ladder", "ladder", poly([[601, 314], [602, 313], [621, 313], [622, 314], [622, 318], [615, 469], [593, 469], [592, 464], [594, 415], [600, 329]]), M.ladder, "N",
      { plane: "ladder", when: (g) => !down(g) }),
    thing("scaffold", "scaffolding", poly([[560, 454], [460, 454], [452, 445], [451, 354], [456, 350], [458, 349], [560, 349], [566, 351], [571, 353], [570, 443]]), M.crew, "N", { plane: "scaffold" }),
    thing("tub", "tub of lime", poly([[543, 452], [543, 467], [507, 469], [499, 467], [497, 466], [497, 451], [498, 450], [512, 437], [515, 437], [542, 451]]), [520, 484], "N", { plane: "tub" }),
    { id: "buckets", name: "buckets of lime", poly: [[563, 491], [536, 507], [521, 507], [493, 496], [489, 493], [488, 475], [495, 465], [554, 461], [560, 464], [565, 473]],
      walkTo: [526, 520], face: "N", look: bucketsLook, use: bucketsUse, when: crewOut },
    { id: "guards", name: "gate guards", verb: "Talk to", poly: [[621, 452], [737, 452], [737, 362], [621, 362]], walkTo: AT_GUARDS, face: "N", look: each("edo.castle.guards"), use: guardsUse },
    // Tomezō: up the ladder (the painter's box round his figure on rung 6), and down at its foot (the box round him there)
    { id: "tomezo", name: "Tomez\u014d", verb: "Talk to", poly: [[586, 400], [626, 400], [626, 322], [586, 322]], walkTo: M.ladder, face: "N",
      look: each("edo.castle.tomezo"), use: tomezoUse, useWith: { trowel: tomezoUse }, when: (g) => !down(g) },
    { id: "tomezo", name: "Tomez\u014d", verb: "Talk to", rect: [608, 380, 32, 92], walkTo: TALK_TOMEZO, face: "E",
      look: each("edo.castle.tomezo"), use: tomezoUse, useWith: { trowel: tomezoUse }, when: (g) => down(g) && crewOut(g) },
    thing("pilgrims", "people on the road", poly([[0, 560], [800, 556], [800, 598], [0, 598]]), M.road, "S"),
    thing("cherry", "double cherry", poly([[0, 346], [0, 206], [2, 157], [12, 67], [24, 48], [34, 42], [173, 10], [181, 10], [213, 11], [233, 18], [239, 23], [241, 27], [275, 118], [277, 224], [277, 232], [272, 398], [264, 443], [105, 549], [80, 551], [72, 551]]), M.cherry, "N",
      { plane: "cherry", use: { lilsis: cherryUse, mom: "edo.castle.cherry.use.mom", bigsis: "edo.castle.cherry.use.bigsis" } }),
    // the petals in the air under the boughs (over the cherry there: a look at them, and catching one)
    thing("petals", "falling petals", poly([[176, 388], [292, 388], [296, 470], [180, 470]]), M.underBoughs, "N"),
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and as the stage is built for anything.
  setup(g) {
    dressAll(g, outfit(g));
    // the two on the lifts: at the scaffold's depth, in front of it; trowelling the wall. The one at the tub: the mixing pole.
    for (const id of ["plasterer3", "plasterer4"]) { const a = g.actor(id); if (a) { a.base = LIFT_BASE; a.hold(true, "trowelwall"); } }
    { const a = g.actor("plasterer2"); if (a) a.hold(true, "trowelwall"); }
    { const a = g.actor("plasterer1"); if (a) a.hold(true, "mix"); }
    { const t = g.actor("tomezo"); if (t && t.kind === "tomezo-ladder") t.base = LADDER_BASE; }
    work.next = {};
    road.walker = null; road.next = 9000;
    CHAT.reset();
  },
};

// (the names a test or a tool may want: the marks and the people's places, as the scene has them)
export const PLACES = { M, LADDER_FOOT, RUNG6, TOMEZO_DOWN, TALK_TOMEZO, AT_GUARDS, LIFT1, LIFT2, MIXER, P2, BUCKETS, THROUGH, PILGRIMS };
export { TOMEZO as tomezoTalk, GUARDS as guardsTalk, CHAT as castleChat, holderOf };

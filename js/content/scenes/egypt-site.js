// Act One, the second of four scenes: the foot of the Great Pyramid, the building site.
// Egypt, about 1920 B.C. (the Bible's own count of years: briefs/DATING.md). Dad plays.
//
// Work has stopped: a wall inside has begun to hum and the men will not go near it. The way in is up the
// stair on the shaded face, and the guard at its foot lets nobody up who is not on the scribe's list.
//
//   chain A   The scribe's pen has split and his last clean sheet is spoken for. Give him the reed and he can
//             write again; give him the road map and he writes Dad a pass on the back of it. Show the pass to
//             the guard and climb to the entrance (to egypt-gallery).
//   chain C1  Later, when Dad knows that light opens the door: the windshield shade, held up on the sunny spot,
//             throws the sun into the entrance. Somebody has to hold it. The guard will, for a cold drink.
//
// The overseer is the running joke and the hint-giver: ask him about the schedule at any point and he says,
// in his own way, what is holding it up. The haulers put Dad right about who builds a pyramid.
// The stair is not walked by clicking on it: the entrance takes Dad up it, once the guard lets him.
//
// Things here that are no part of any puzzle:
//   - The scribe's news (ask him for it: "Any news?"). As the grumble of a man who keeps the grain account, he tells
//     this week's palace gossip, from outside, with no idea whom he is talking about: famine across the desert, a
//     rich herdsman called Abram and his sister, taken into the Great House; the sickness there since; the word that
//     she is his WIFE; the king sending him away this morning. Genesis 12:10-20. Dad understands slowly, and then all
//     at once: he is standing in Genesis 12. He would give a lot to go and shake that man's hand, and he has a boy to
//     find. Told once ("egypt.heardAbram"); from then on he knows when he is, and the river, the reeds and the open
//     door say so. Nobody meets Abram or Sarai; nobody of the time says anything about Abram's God.
//   - The mud bricks: he half remembers that Israel made bricks for Pharaoh, looks up at the stone, and is put right
//     by the text of Exodus (not by a person; nobody of the time speaks of Israel).
//   - The masons' stone, looked at again: seashells in it, in the desert. The Flood (Genesis 7:19-20), and Mizraim,
//     Noah's grandson (Genesis 10:6), whose name the country has. Said once.
//   - The doorway: the first time he reaches it, before he goes into the dark, he prays (the second of his three
//     prayers in the act).
//   - General Feathers: the scribe and the guard each have something to say about her, once.
//
// Try it: index.html?scene=egypt-site&lead=dad
// Later states: &flags=egypt.arrived,egypt.sawSite,egypt.hasPass,egypt.inside,egypt.knowsLight

const art = "art/scenes/egypt-site/";

/** How many times a line has been spoken. (The engine counts every line it says.) */
const count = (g, id) => g.store.data.seenLines[id] || 0;
/** A thing worth looking at twice: the first line, then the second, turn about. */
const twice = (first, second) => (g) => g.say(count(g, first) <= count(g, second) ? first : second);
/** Of several lines, the one heard least: a person with a few things to say says them in turn. */
const least = (g, ids) => ids.reduce((best, id) => (count(g, id) < count(g, best) ? id : best));
/** Someone who can stand turns to Dad. */
const turnTo = (g, who) => { const a = g.actor(who), me = g.lead; if (a && me) a.look(me.x, me.y); };
/** Is the sunbeam complete: shade outside, door mirror at the foot of the gallery, copper mirror at the top? */
const allSet = (g) => !!(g.flag("egypt.shadeSet") && g.flag("egypt.footSet") && g.flag("egypt.topSet"));
/** Dad keeps his arm out, as at the top of a reach, until told to drop it: he is holding something up. */
const holdOut = (g, on) => { if (g.lead) g.lead.hold(on); };
/** Head bowed, hands folded (true), or let it go (false). A figure that has no such pose simply stands. */
const pray = (a, on) => a && a.pray && a.pray(on);
/** General Feathers, shown to somebody: he introduces her, and they answer, once, in their own way. After that (and
    for anybody with no answer of their own) Dad's stock reply. `answer` is their line, and Dad's comeback if any. */
const showGeneral = (who, ...answer) => async (g) => {
  turnTo(g, who);
  if (count(g, answer[0])) return g.say("egypt.chicken.stock");
  await g.say("egypt.chicken.show", ...answer);
};

// ---------- light: the sunbeam from the shade up into the entrance ----------
// The painter's line for it runs from the middle of the shade (391, 406) to the middle of the doorway (542, 229).
const BEAM = [[380, 396], [402, 416], [548, 234], [536, 224]];        // the soft outer light (it narrows with distance)
const CORE = [[386, 402], [396, 410], [544, 231], [540, 227]];        // its bright middle
const points = (shape) => shape.map((p) => p.join(",")).join(" ");
/** Show or hide a part of the light at once (setup), or bring it up or down over a moment (scripts). */
const lit = (g, id, on) => { const el = g.q("#" + id); if (el) el.setAttribute("opacity", on ? 1 : 0); };
const glow = (g, id, ms = 900, to = 1) => { const el = g.q("#" + id); return el ? g.tween(ms, (k) => el.setAttribute("opacity", to ? k : 1 - k)) : Promise.resolve(); };

// ---------- the stair ----------
// Nobody walks onto the stair by clicking: a script takes Dad up it and down it, along the painter's own marks for his feet.
const STAIR = [[716, 400], [692, 360], [670, 326], [652, 296], [636, 269]];     // the painted steps, foot first
const LANDING = [[627, 269], [586, 267], [552, 266]];                         // and along the landing to the doorway

/** Draw someone as another figure from js/art/people.js (the same man in another pose), keeping his id, his place
    and the way he faces. If that figure has not been drawn yet, he stays as he is. */
function redraw(g, id, kind) {
  const cast = g.view.cast, old = g.actor(id);
  if (!old || old.kind === kind) return;
  cast.remove(id);
  try { cast.addFigure(id, kind, old.x, old.y, old.scale).face(old.yaw); }
  catch { cast.add(old); }
}

// ---------- chain A: the scribe ----------
async function talkToScribe(g) {
  if (!g.flag("egypt.metScribe")) {
    if (!g.flag("egypt.penGiven")) await g.say("egypt.scribe.meet.1", "egypt.scribe.meet.2", "egypt.scribe.meet.3");
    g.flag("egypt.metScribe", true);
  }
  for (;;) {
    const pick = await g.choose([
      { id: "boy", line: "egypt.ask.boy" },
      { id: "list", line: "egypt.scribe.ask.list" },
      { id: "news", line: "egypt.scribe.ask.news", when: (g) => !g.flag("egypt.heardAbram") },      // told once
      { id: "bye", line: "egypt.ask.bye" },
    ]);
    if (pick === "boy") await g.say("egypt.ask.boy", "egypt.scribe.boy.1", "egypt.scribe.boy.2");
    else if (pick === "list") await g.say("egypt.scribe.ask.list", g.flag("egypt.hasPass") ? "egypt.scribe.list.done" : g.flag("egypt.penGiven") ? "egypt.scribe.list.nosheet" : "egypt.scribe.list.nopen");
    else if (pick === "news") return news(g);                 // he has heard what he needed to hear, and he goes
    else return g.say("egypt.ask.bye", "egypt.ans.bye");
  }
}

// ---------- the news: Abram is in Egypt ----------
/** The scribe's grumble about the grain account turns into this week's gossip from the palace. He has no idea whom
    he is talking about. Dad understands slowly, then all at once; then he looks out the way the man has gone, and
    back up at the doorway his son went in by. Genesis 12:10-20, told from outside; nobody meets Abram or Sarai. */
async function news(g) {
  turnTo(g, "scribe");
  await g.say("egypt.scribe.ask.news", "egypt.scribe.news.1", "egypt.scribe.news.2", "egypt.scribe.news.3", "egypt.scribe.news.4", "egypt.scribe.news.5");
  await g.say("egypt.scribe.news.6", "egypt.scribe.news.7", "egypt.scribe.news.8", "egypt.scribe.news.9", "egypt.scribe.news.10");
  g.flag("egypt.heardAbram", true);
  await g.wait(400);
  g.lead.look(40, 300);                           // out across the desert, the way the man has gone
  await g.wait(500);
  await g.say("egypt.abram.1", "egypt.abram.2", "egypt.abram.3", "egypt.abram.4");
  await g.wait(300);
  g.lead.look(541, 234);                          // and back up at the doorway
  await g.wait(400);
  await g.say("egypt.abram.5");
}

async function giveReed(g) {
  await g.say("egypt.give.reed");
  await g.reach();
  g.take("reed");
  await g.say("egypt.got.reed", "egypt.scribe.rush", "egypt.scribe.supplier", "egypt.scribe.needsheet");
  g.flag("egypt.metScribe", true);
  g.flag("egypt.penGiven", true);
}

async function giveMap(g) {
  await g.say("egypt.give.map");
  if (!g.flag("egypt.penGiven")) return g.say("egypt.got.map.nopen");
  await g.reach();
  g.take("map");
  await g.wait(700);                              // he writes
  await g.say("egypt.scribe.pass.1", "egypt.scribe.pass.2");
  await g.reach();
  g.give("pass");
  g.flag("egypt.hasPass", true);
  await g.say("egypt.pass.got");
}

// ---------- chain A: the guard and the stair ----------
async function turnedBack(g) {
  turnTo(g, "guard");
  if (g.flag("egypt.metGuard")) return g.say("egypt.guard.stop");
  await g.say("egypt.guard.stop", "egypt.guard.stop.2", "egypt.guard.stop.3");
  g.flag("egypt.metGuard", true);
}

async function showPass(g) {
  turnTo(g, "guard");
  await g.say("egypt.pass.show");
  await g.reach();
  await g.say("egypt.guard.pass.1", "egypt.guard.pass.2");
  g.flag("egypt.metGuard", true);
  g.flag("egypt.inside", true);                   // from now on the stair is his to climb
  await upTheStair(g);
}

/** The whole climb is shown once, and at the top of it he prays before he goes in. It is a long stair: after that,
    the picture changes when he is a few steps up. */
async function upTheStair(g) {
  const all = [...STAIR, ...LANDING], far = g.flag("egypt.climbed") ? 3 : all.length;
  await g.walkTo(...STAIR[0]);
  for (const [x, y] of all.slice(1, far)) await g.moveTo(x, y);
  if (far === all.length) {                       // at the doorway, the first time: he stops at the dark, and prays
    g.lead.face("W");
    await g.wait(350);
    pray(g.lead, true);
    await g.wait(400);
    await g.say("egypt.site.pray.1", "egypt.site.pray.2");
    pray(g.lead, false);
    await g.wait(350);
    g.lead.face("N");                             // and turns to go in
  }
  g.flag("egypt.climbed", true);
  await g.goto("egypt-gallery", { spawn: "fromSite" });
}

/** Down the steps to the sand, from wherever on them he is: the doorway the first time, halfway down after that. */
async function downTheStair(g) {
  const all = [...STAIR, ...LANDING].reverse(), at = all.findIndex(([, y]) => y >= g.lead.y - 2);
  for (const [x, y] of all.slice(Math.max(at, 0))) await g.moveTo(x, y);
  await g.walkTo(742, 424);                       // a step clear of the foot of the stair
  g.flag("egypt.cameDown", true);
}

/** The entrance and the stair: up he goes, if the guard lets him. */
async function climb(g) {
  if (g.flag("egypt.inside")) return upTheStair(g);
  return g.has("pass") ? showPass(g) : turnedBack(g);
}

async function talkToGuard(g) {
  if (g.flag("egypt.shadeSet")) return g.say(least(g, ["egypt.guard.arms.1", "egypt.guard.arms.2", "egypt.guard.arms.3"]));
  if (!g.flag("egypt.inside")) return g.has("pass") ? showPass(g) : turnedBack(g);
  turnTo(g, "guard");
  return g.say(g.flag("egypt.guardDrank") ? "egypt.guard.owe" : "egypt.guard.after");
}

// ---------- chain C1: the shade, the sunny spot, and somebody to stand there ----------
/** Dad holds the shade up himself. It works, and it shows him what he needs: somebody else to do it. */
async function tryShade(g) {
  const shade = g.plane("shade");
  await g.reach();
  try {
    holdOut(g, true);
    if (shade) shade.show(true);                  // the shade, up in the sun
    await glow(g, "beam-site", 450);
    await g.say("egypt.shade.try.1");
    await glow(g, "beam-site", 350, 0);
  } finally {                                     // whatever happens, he is not left holding it
    lit(g, "beam-site", false);
    if (shade) shade.show(false);
    holdOut(g, false);
  }
  await g.say("egypt.shade.try.2");
}

/** The shade, offered to the guard. He holds nothing until he has had something cold. */
async function askGuard(g) {
  turnTo(g, "guard");
  if (g.flag("egypt.guardDrank")) { await g.say("egypt.shade.favor"); return holdShade(g); }
  await g.say("egypt.shade.ask", "egypt.guard.nohold", "egypt.guard.cold");
  g.flag("egypt.guardAsked", true);
}

/** A root beer for the guard. If Dad has the shade with him, the bargain is done on the spot; if not, the guard owes him one. */
async function giveRootbeer(g) {
  turnTo(g, "guard");
  if (g.flag("egypt.guardDrank")) return g.say("egypt.guard.again");
  await g.say("egypt.rootbeer.give");
  await g.reach();
  g.take("rootbeer");
  await g.say("egypt.guard.rootbeer");
  g.flag("egypt.guardDrank", true);
  if (!g.has("shade")) return g.say("egypt.guard.owe");
  await holdShade(g);
}

/** The guard takes the shade to the sunny spot, and the sun goes up the stair and in at the door. */
async function holdShade(g) {
  if (!g.flag("egypt.guardAsked")) {              // he has not been told yet what he is to hold, or where
    await g.say("egypt.shade.ask");
    g.flag("egypt.guardAsked", true);
  }
  await g.say("egypt.guard.take", "egypt.shade.notlong", "egypt.guard.notlong");
  await g.reach();
  g.take("shade");
  await g.walkTo(330, 520, "guard");              // the sunny spot (he goes round the sledge)
  const guard = g.actor("guard"), shade = g.plane("shade");
  if (guard) guard.face("E");
  redraw(g, "guard", "guard-shade");              // his arms go up
  if (shade) shade.show(true);                    // and the shade is in his hands
  g.flag("egypt.shadeSet", true);
  g.lead.look(330, 520);
  await glow(g, "beam-site");
  await g.say("egypt.shade.lit");
  if (allSet(g)) await g.say("egypt.beam.all");
  turnTo(g, "overseer");
  await g.say("egypt.overseer.bark.guard");
}

// ---------- the mud bricks ----------
/** He lifts one, and half remembers: Israel made bricks for Pharaoh. Then he looks up at the pyramid, which is stone,
    and does the arithmetic out loud (Exodus 1:11, 1:14, 5:7). Said once; after that the bricks are only bricks. */
async function liftBrick(g) {
  if (count(g, "egypt.site.bricks.use.1")) return g.say("egypt.site.bricks.look");
  await g.reach(true);
  await g.say("egypt.site.bricks.use.1");
  g.lead.look(700, 180);                          // up at the pyramid
  await g.wait(350);
  await g.say("egypt.site.bricks.use.2", "egypt.site.bricks.use.3", "egypt.site.bricks.use.4");
}

// ---------- the masons' stone: seashells in the desert ----------
/** The first look is at the tools. The second is at the stone they are cutting, which is full of little round shells:
    the Flood was here first (Genesis 7:19-20), and Noah's grandson after it (Genesis 10:6). Said once; after that the
    tools are only tools. */
async function lookAtStone(g) {
  if (count(g, "egypt.site.blocks.look") && !count(g, "egypt.site.shells.1")) return g.say("egypt.site.shells.1", "egypt.site.shells.2", "egypt.site.mizraim");
  await g.say("egypt.site.blocks.look");
}

// ---------- the overseer ----------
/** The schedule, as it stands. This is also where the player is told, in the overseer's way, what to do next. */
function report(g) {
  if (allSet(g)) return g.say("egypt.overseer.sched.4", "egypt.overseer.sched.4b", "egypt.overseer.sched.4c");
  if (g.flag("egypt.knowsLight")) return g.say("egypt.overseer.sched.3", "egypt.overseer.sched.3b", "egypt.overseer.sched.3c");
  if (g.flag("egypt.heardBoy")) return g.say("egypt.overseer.sched.2");
  if (g.flag("egypt.inside")) return g.say("egypt.overseer.sched.1");
  return g.say("egypt.overseer.sched.0a", "egypt.overseer.sched.0b");
}

async function talkToOverseer(g) {
  turnTo(g, "overseer");
  if (!g.flag("egypt.metOverseer")) {
    await g.say("egypt.overseer.meet.1", "egypt.overseer.meet.2", "egypt.overseer.meet.3");
    g.flag("egypt.metOverseer", true);
  }
  for (;;) {
    const pick = await g.choose([
      { id: "boy", line: "egypt.ask.boy" },
      { id: "hum", line: "egypt.overseer.ask.hum" },
      { id: "schedule", line: "egypt.overseer.ask.schedule" },
      { id: "bye", line: "egypt.overseer.ask.bye" },
    ]);
    if (pick === "boy") await g.say("egypt.ask.boy", "egypt.overseer.boy.1");
    else if (pick === "hum") await g.say("egypt.overseer.ask.hum", "egypt.overseer.hum.1", "egypt.overseer.hum.2", "egypt.overseer.hum.3", "egypt.overseer.hum.4");
    else if (pick === "schedule") { await g.say("egypt.overseer.ask.schedule"); await report(g); }
    else return g.say("egypt.overseer.ask.bye", "egypt.overseer.bye");
  }
}

// ---------- the haulers: one speaks, one agrees, one eats ----------
async function talkToHaulers(g) {
  for (const who of ["hauler1", "hauler2", "hauler3"]) turnTo(g, who);
  if (!g.flag("egypt.metHaulers")) {
    await g.say("egypt.haulers.meet.1", "egypt.haulers.meet.2", "egypt.haulers.meet.3");
    g.flag("egypt.metHaulers", true);
  }
  for (;;) {
    const pick = await g.choose([
      { id: "boy", line: "egypt.ask.boy" },
      { id: "break", line: "egypt.haulers.ask.break" },
      { id: "free", line: "egypt.haulers.ask.free" },
      { id: "sand", line: "egypt.haulers.ask.sand" },
      { id: "bye", line: "egypt.haulers.ask.bye" },
    ]);
    if (pick === "boy") await g.say("egypt.ask.boy", "egypt.haulers.boy.1", "egypt.haulers.boy.2", "egypt.haulers.boy.3");
    else if (pick === "break") await g.say("egypt.haulers.ask.break", "egypt.haulers.break.1", "egypt.haulers.break.2");
    else if (pick === "free") await g.say("egypt.haulers.ask.free", "egypt.haulers.free.1", "egypt.haulers.free.2", "egypt.haulers.free.3", "egypt.haulers.free.4");
    else if (pick === "sand") await g.say("egypt.haulers.ask.sand", "egypt.haulers.sand.1", "egypt.haulers.sand.2");
    else return g.say("egypt.haulers.ask.bye", "egypt.haulers.bye.1", "egypt.haulers.bye.2");
  }
}

export default {
  id: "egypt-site",
  era: "egypt",
  name: "At the foot of the pyramid",

  // Every number below is a pixel of the painting, measured by the painter (art/scenes/egypt-site/layout.json).
  // DEPTH. minScale is Dad's size on the steps and the landing, where it fits the doorway.
  horizon: 250, full: 590, minScale: 0.33,

  // The trampled sand, and with it the steps and the landing (so that Dad can stand on them). The first thing in
  // `blocked` is a bar across the bottom steps: it cuts the stair off from the sand, so that no click can send him
  // up it. Only the scripts above cross it. The rest are the scribe's station, the sledge, the drying bricks and a jar.
  walk: { area: [[0, 578], [0, 398], [120, 392], [212, 381], [248, 378], [318, 381], [405, 376], [487, 372], [515, 372], [616, 372], [635, 381], [670, 399], [696, 396], [678, 365], [661, 337], [647, 312], [634, 290], [622, 269], [622, 274], [512, 273], [512, 261], [649, 262], [649, 269], [663, 290], [677, 312], [693, 337], [711, 365], [731, 396], [752, 409], [800, 411], [800, 506], [722, 504], [612, 516], [552, 572], [544, 596], [122, 596], [112, 587]] },
  blocked: [
    [[686, 382], [728, 382], [728, 388], [686, 388]],
    [[54, 475], [224, 473], [245, 437], [103, 439]],
    [[397, 466], [563, 481], [571, 460], [419, 448]],
    [[524, 398], [604, 392], [606, 380], [526, 384]],
    [[360, 472], [384, 472], [384, 462], [360, 462]],
  ],
  spawn: {
    default: [170, 574],
    fromCrash: [170, 574],          // up the track from the river, bottom left
    fromGallery: [552, 266],        // out of the doorway, on the landing (enter() brings him down the steps)
    fromGalleryAgain: [670, 326],   // every time after the first: already halfway down them
  },
  exits: ["egypt-crash", "egypt-gallery"],

  picture: art + "back.png",

  planes: [
    { id: "awning", src: art + "awning.png", base: 474 },
    { id: "sledge", src: art + "sledge.png", base: [[420, 467], [559, 479]] },
    { id: "shade", src: art + "shade.png", base: 521, when: (g) => !!g.flag("egypt.shadeSet"),        // in the hands of the man on the sunny spot,
      solid: [[305, 508], [355, 508], [355, 528], [305, 528]] },                                      // who takes up that patch of sand while he holds it
    { id: "front", src: art + "front.png", plane: "front" },
  ],

  // The sunbeam is light, so it is drawn live and stays smooth: a glow round the shade, the beam, and the doorway lit.
  // setup() shows it if the shade is already up.
  live() {
    return `<defs><filter id="sun-soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
        <filter id="sun-edge" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.6"/></filter></defs>
      <g id="beam-site" opacity="0" shape-rendering="geometricPrecision">
        <ellipse cx="394" cy="405" rx="62" ry="27" transform="rotate(-29 394 405)" fill="#fff6cf" opacity="0.6" filter="url(#sun-soft)"/>
        <polygon points="${points(BEAM)}" fill="#ffe7a0" opacity="0.3" filter="url(#sun-soft)"/>
        <polygon points="${points(CORE)}" fill="#fff4c8" opacity="0.55" filter="url(#sun-edge)"/>
        <ellipse cx="541" cy="234" rx="15" ry="27" fill="#ffe9ae" opacity="0.5" filter="url(#sun-soft)"/>
      </g>`;
  },

  actors: [
    { id: "scribe", kind: "scribe", at: [150, 448], face: "E" },
    { id: "overseer", kind: "overseer", at: [470, 520], face: "W" },         // in front of his stalled sledge
    { id: "hauler3", kind: "hauler3", at: [270, 394], face: "S" },
    { id: "hauler2", kind: "hauler2", at: [296, 405], face: "S" },
    { id: "hauler1", kind: "hauler1", at: [322, 416], face: "SW" },
    { id: "guard", kind: "guard", at: [690, 420], face: "SW", when: (g) => !g.flag("egypt.shadeSet") },      // at the foot of the stair
    { id: "guard", kind: "guard", at: [330, 520], face: "E", when: (g) => !!g.flag("egypt.shadeSet") },      // on the sunny spot, holding the shade
  ],

  // Make the picture match the story facts. Runs on arrival and after loading a save.
  setup(g) {
    lit(g, "beam-site", g.flag("egypt.shadeSet"));
    if (g.flag("egypt.shadeSet")) redraw(g, "guard", "guard-shade");
  },

  // The far things first: an area lower in this list lies over the ones above it.
  hotspots: [
    { id: "pyramid", name: "pyramid", poly: [[268, 334], [341, 0], [800, 0], [800, 316]], look: twice("egypt.site.pyramid.look", "egypt.site.pyramid.look2") },
    { id: "small-pyramids", name: "small pyramids", rect: [0, 228, 176, 56], look: "egypt.site.small.look" },
    { id: "yard", name: "stone yard", rect: [24, 280, 140, 48], look: "egypt.site.yard.look" },
    { id: "scaffold", name: "scaffold", rect: [640, 60, 160, 300], look: "egypt.site.scaffold.look" },
    {
      id: "stair", name: "stairs", verb: "Climb", poly: [[686, 400], [746, 400], [659, 269], [613, 269]], walkTo: [742, 424], face: "W",
      look: "egypt.site.stair.look", use: climb, useWith: { pass: climb },
    },
    {
      id: "entrance", name: "entrance", verb: "Climb to", rect: [515, 195, 52, 75], walkTo: [742, 424], face: "W",
      look: (g) => g.say(g.flag("egypt.inside") ? "egypt.site.entrance.look2" : "egypt.site.entrance.look"), use: climb, useWith: { pass: climb },
    },
    { id: "bricks", name: "mud bricks", verb: "Lift", rect: [520, 376, 96, 24], walkTo: [560, 410], face: "N", look: "egypt.site.bricks.look", use: liftBrick },
    { id: "scribe-desk", name: "scribe's station", rect: [52, 332, 195, 145], walkTo: [248, 464], face: "W", look: twice("egypt.site.desk.look", "egypt.site.desk.look2") },
    { id: "rope", name: "hauling rope", poly: [[392, 444], [400, 460], [300, 414], [226, 388], [222, 374], [300, 396]], walkTo: [352, 440], face: "NW", look: "egypt.site.rope.look" },
    { id: "sledge", name: "sledge", verb: "Pull", rect: [395, 379, 177, 102], walkTo: [420, 492], face: "NE", look: twice("egypt.site.sledge.look", "egypt.site.sledge.look2"), use: "egypt.site.sledge.use" },
    { id: "blocks", name: "masons' tools", verb: "Borrow", poly: [[561, 486], [636, 447], [800, 440], [800, 600], [556, 600]], walkTo: [538, 566], face: "E", look: lookAtStone, use: "egypt.site.blocks.use" },
    {
      id: "sunspot", name: "sunny spot", verb: "Stand in", rect: [296, 504, 70, 30], walkTo: [330, 520], face: "E", when: (g) => !g.flag("egypt.shadeSet"),
      look: (g) => g.say(g.flag("egypt.knowsLight") ? "egypt.site.sunspot.look2" : "egypt.site.sunspot.look"), use: "egypt.site.sunspot.use",
      useWith: { shade: tryShade },
    },
    { id: "water", name: "water jars", rect: [0, 494, 100, 40], walkTo: [130, 590], face: "W", look: "egypt.site.water.look" },      // the shoulders of the jars: below them the corner is the way out
    {
      id: "track", name: "track to the river", verb: "Walk down", poly: [[0, 520], [150, 540], [176, 600], [0, 600]], walkTo: [130, 590], face: "W",
      look: "egypt.site.track.look", use: (g) => g.goto("egypt-crash", { spawn: "fromSite" }),
    },
    {
      id: "haulers", name: "haulers", verb: "Talk to", poly: [[256, 322], [338, 330], [340, 418], [304, 418], [256, 396]], walkTo: [352, 440], face: "NW",
      look: "egypt.haulers.look", use: talkToHaulers,
      useWith: {
        rootbeer: ["egypt.haulers.rootbeer.1", "egypt.haulers.rootbeer.2", "egypt.haulers.rootbeer.3", "egypt.haulers.rootbeer.4"],
        shade: ["egypt.haulers.shade.1", "egypt.haulers.shade.2"],
        chicken: "egypt.chicken.stock",
      },
    },
    {
      id: "overseer", name: "overseer", verb: "Talk to", rect: [444, 386, 54, 136], walkTo: [404, 532], face: "E",
      look: "egypt.overseer.look", use: talkToOverseer,
      useWith: { map: "egypt.overseer.map", shade: "egypt.overseer.shade", carmirror: "egypt.overseer.mirror", coppermirror: "egypt.overseer.mirror", rootbeer: "egypt.overseer.rootbeer", chicken: "egypt.chicken.stock" },
    },
    {
      id: "scribe", name: "scribe", verb: "Talk to", rect: [124, 392, 52, 58], walkTo: [248, 464], face: "W",
      look: (g) => g.say(g.flag("egypt.penGiven") ? "egypt.scribe.look2" : "egypt.scribe.look"), use: talkToScribe,
      useWith: { reed: giveReed, map: giveMap, rootbeer: "egypt.scribe.rootbeer", shade: "egypt.scribe.shade", pass: "egypt.scribe.pass", chicken: showGeneral("scribe", "egypt.scribe.chicken") },
    },
    {
      id: "guard", name: "guard", verb: "Talk to", rect: [672, 326, 36, 96], walkTo: [742, 424], face: "W", when: (g) => !g.flag("egypt.shadeSet"),
      look: "egypt.guard.look", use: talkToGuard,
      useWith: {
        pass: (g) => (g.flag("egypt.inside") ? g.say("egypt.guard.after") : showPass(g)),
        shade: askGuard, rootbeer: giveRootbeer, sunglasses: "egypt.guard.sunglasses", map: "egypt.guard.map",
        chicken: showGeneral("guard", "egypt.guard.chicken", "egypt.guard.chicken.2"),
      },
    },
    {
      id: "guard-sun", name: "guard", verb: "Talk to", poly: [[308, 380], [352, 380], [350, 411], [439, 374], [444, 383], [424, 406], [354, 435], [352, 522], [308, 522]], walkTo: [268, 534], face: "E", when: (g) => !!g.flag("egypt.shadeSet"),
      look: "egypt.guard.look2", use: talkToGuard,
      useWith: { rootbeer: "egypt.guard.full", sunglasses: "egypt.guard.sunglasses", chicken: showGeneral("guard", "egypt.guard.chicken", "egypt.guard.chicken.2") },
    },
  ],

  // Runs when the lead arrives, and again when a save is loaded (then `from` is null). It must be safe to run twice,
  // so each part checks its own fact.
  async enter(g, from) {
    if (g.lead.y < 380) await downTheStair(g);    // he has come out of the doorway
    if (!g.flag("egypt.sawSite")) {
      await g.wait(400);
      await g.say("egypt.site.arrive.1", "egypt.site.arrive.2", "egypt.site.arrive.3");
      g.flag("egypt.sawSite", true);
      return;
    }
    // The overseer keeps count of what his specialist has done, and calls out when he sees him come back. Each of
    // these is said once, and only on a real arrival: a loaded save does not set him off.
    if (!from) return;
    if (allSet(g) && !g.flag("egypt.barkAll")) {
      await g.say("egypt.overseer.bark.all");
      g.flag("egypt.barkAll", true);
    } else if (g.flag("egypt.knowsLight") && !g.flag("egypt.barkLight") && !allSet(g)) {
      await g.say("egypt.overseer.bark.light");
      g.flag("egypt.barkLight", true);
    }
  },
};

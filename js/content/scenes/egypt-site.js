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
//   - The scribe's news (ask him for it: "Any news?"; offered once Lot, down by the river, has told Dad who he is:
//     "egypt.heardAbram"). As the grumble of a man who keeps the grain account, he tells this week's palace gossip,
//     the Egyptian side of the story Lot told, from outside, with no idea whom he is talking about: famine across the
//     desert, a rich herdsman called Abram and his sister, taken into the Great House; the king's gifts; the sickness
//     there since; the word that she is his WIFE; the king sending him away today, in a hurry. Genesis 12:10-20. Dad
//     hears it knowing more than the scribe does (he has met the man's nephew; he knows what "Pharaoh" means, and how
//     the story is written), and finishes on the man by the river, praying for his boy. Told once. Nobody meets Abram
//     or Sarai; no Egyptian says anything about Abram's God.
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
      { id: "news", line: "egypt.scribe.ask.news", when: (g) => !!g.flag("egypt.heardAbram") && !count(g, "egypt.scribe.ask.news") },      // once Lot has told him; told once
      { id: "bye", line: "egypt.ask.bye" },
    ]);
    if (pick === "boy") await g.say("egypt.ask.boy", "egypt.scribe.boy.1", "egypt.scribe.boy.2");
    else if (pick === "list") await g.say("egypt.scribe.ask.list", g.flag("egypt.hasPass") ? "egypt.scribe.list.done" : g.flag("egypt.penGiven") ? "egypt.scribe.list.nosheet" : "egypt.scribe.list.nopen");
    else if (pick === "news") return news(g);                 // he has heard what he needed to hear, and he goes
    else return g.say("egypt.ask.bye", "egypt.ans.bye");
  }
}

// ---------- the news: the same week, from the Egyptian side ----------
/** The scribe's grumble about the grain account turns into this week's gossip from the palace. He has no idea whom
    he is talking about; Dad, who has met the man's nephew by the river, does, and knows how the story is written.
    At the end he looks back down the track to the river. Genesis 12:10-20, told from outside; nobody meets Abram or Sarai. */
async function news(g) {
  turnTo(g, "scribe");
  await g.say("egypt.scribe.ask.news", "egypt.scribe.news.1", "egypt.scribe.news.2", "egypt.scribe.news.3", "egypt.scribe.news.4", "egypt.scribe.news.5");
  await g.say("egypt.scribe.news.6", "egypt.scribe.news.7", "egypt.scribe.news.8", "egypt.scribe.news.9", "egypt.scribe.news.10");
  await g.wait(400);
  g.lead.look(60, 590);                           // back down the track, toward the river
  await g.wait(450);
  if (g.flag("egypt.lotPrayed")) await g.say("egypt.scribe.news.11");     // (Lot has prayed for the boy: in a game played straight through he always has by now)
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

/** The three haulers are one conversation, and three shapes: each man is outlined as himself. */
const HAULERS = {
  name: "haulers", verb: "Talk to", walkTo: [352, 440], face: "NW",
  look: "egypt.haulers.look", use: talkToHaulers,
  useWith: {
    rootbeer: ["egypt.haulers.rootbeer.1", "egypt.haulers.rootbeer.2", "egypt.haulers.rootbeer.3", "egypt.haulers.rootbeer.4"],
    shade: ["egypt.haulers.shade.1", "egypt.haulers.shade.2"],
    chicken: "egypt.chicken.stock",
  },
};

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
  // The bottom of the picture is the way back down to the river: a click anywhere along it, and down he goes.
  edges: {
    S: { to: "egypt-crash", spawn: "fromSite", name: "down to the river" },
  },

  picture: art + "back.png",

  planes: [
    { id: "awning", src: art + "awning.png", base: 474 },
    { id: "sledge", src: art + "sledge.png", base: [[420, 467], [559, 479]] },
    { id: "shade", src: art + "shade.png", base: 521, when: (g) => !!g.flag("egypt.shadeSet"),        // in the hands of the man on the sunny spot,
      solid: [[305, 508], [355, 508], [355, 528], [305, 528]] },                                      // who takes up that patch of sand while he holds it
    { id: "front", src: art + "front.png", plane: "front" },
    // The gang's standard's two streamers (round four), lifted out of the picture so that they can stir in the wind; the
    // pole and its board stay in back.png.
    { id: "streamers", src: art + "streamers.png", base: 398 },
  ],

  // THINGS THAT MOVE BY NATURE (round four: briefs/out/paint-4b-ready.md). Nothing that moves is painted still: the
  // painter took them out of the picture and marked where they go (layout.json, "fx"), and the engine draws them moving.
  fx: [
    // bread ovens' smoke in the builders' town far off beyond the plateau's lip: it rises behind the queens' pyramids,
    // which let a fifth of it show through, as haze
    ...[[20, 275, 279], [88, 269, 273], [140, 263, 267]].map(([x, y, base], n) => ({ id: `oven-smoke-${n + 1}`, type: "smoke", at: [x, y], base, color: "#f4ecdc", opacity: 0.32, height: 19, width: [1, 5], lean: [20, -17], rate: 2,
      behind: [[[7, 277], [36, 227], [65, 277], [44.7, 280]], [[64, 274], [80.8, 245.3], [95.2, 245.3], [112, 274], [95.2, 277]], [[111, 272], [130, 240], [149, 272], [135.7, 275]]], behindOpacity: 0.2 })),
    // black kites wheeling high in the warm air over the left, mostly gliding (behind everything)
    { id: "kites", type: "birds", kind: "flyers", circle: { at: [186, 74], r: [34, 14] }, count: 3, speed: 12, scale: 0.9, color: "#3a3a4e", size: [5, 9],
      frames: { glide: "kite-0.png", flap: ["kite-1.png", "kite-0.png", "kite-2.png", "kite-0.png"], bank: "kite-3.png", middle: [6.5, 5] } },
    // the standard's two streamers (red, cream) blowing out to the right from the pole
    { id: "streamers", type: "sway", plane: "streamers", anchor: "left", at: [200, 306], amount: 1.5, period: 2.6, wave: 40, lean: 0.1 },
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

  // THEIR OWN LIVES (round four: js/engine/life.js). Everyone fidgets in their own way; the scribe, the overseer and
  // the haulers now and then walk a few steps and come back, one at a time, each in their own time. The scribe's mark
  // is on his mat under the awning, off the sand the family walks on: he gets up there, and walks straight out and back.
  actors: [
    // The scribe sits on his mat. While his pen is split he has nothing to do (writer's block): now and then he gets up,
    // walks out from under the awning to look at the stalled sledge and the pyramid, or down the track for anyone
    // bringing reeds, and sits down again. Once he has a pen he is writing, catching up on a whole morning, and stays.
    { id: "scribe", kind: "scribe", at: [150, 448], face: "E", when: (g) => !g.flag("egypt.penGiven"),
      life: { every: [22, 40], spots: [[232, 488, "NE"], [120, 494, "S"]], stay: [3, 7] } },
    { id: "scribe", kind: "scribe", at: [150, 448], face: "E", when: (g) => !!g.flag("egypt.penGiven"),
      life: { still: true } },
    // The overseer paces in front of his stalled sledge: over toward the haulers to glare at them, or along to look up
    // at the doorway the work is waiting on.
    { id: "overseer", kind: "overseer", at: [470, 520], face: "W",         // in front of his stalled sledge
      life: { every: [16, 30], spots: [[408, 504, "NW"], [528, 540, "N"]], stay: [2.5, 5] } },
    // The haulers are on a break by their rope (one speaks, one agrees, one eats): now and then one of them strolls a few
    // steps and back. They stand so close that the usual patch of ground under each would take in his neighbour's place:
    // each blocks a smaller patch under his own feet, so that he can come home exactly to his mark.
    { id: "hauler3", kind: "hauler3", at: [270, 394], face: "S", solid: [[260, 386], [280, 386], [280, 399], [260, 399]],
      life: { every: [40, 70], spots: [[232, 404, "SW"]], stay: [3, 6] } },
    { id: "hauler2", kind: "hauler2", at: [296, 405], face: "S", solid: [[286, 397], [306, 397], [306, 410], [286, 410]],
      life: { every: [32, 58], spots: [[258, 432, "S"], [338, 444, "SE"]], stay: [3, 7] } },
    { id: "hauler1", kind: "hauler1", at: [322, 416], face: "SW", solid: [[312, 408], [332, 408], [332, 421], [312, 421]],
      life: { every: [28, 52], spots: [[372, 440, "SE"], [360, 412, "E"]], stay: [3, 6] } },
    // Two masons far up the faces, each on a plank slung on ropes (the painter's cradles), facing the stone and rubbing
    // it smooth now and then: small, and never leaving their planks. Their size is the painter's (the plank on the
    // shaded face is 48 pixels wide for a man-and-a-half; the one on the sunlit face, far along it, 21).
    { id: "mason1", kind: "mason1", at: [408, 152], face: "NE", scale: 0.33, life: { still: true, fidget: [4, 9] } },     // (he stands where the painted jar is)
    { id: "mason2", kind: "mason2", at: [257, 206], face: "N", scale: 0.13, life: { still: true, fidget: [5, 11] } },
    // The guard keeps the stair (and, once he has the shade, holds it up on the sunny spot): small movements only.
    { id: "guard", kind: "guard", at: [690, 420], face: "SW", when: (g) => !g.flag("egypt.shadeSet"),      // at the foot of the stair
      life: { still: true, fidget: [5, 12] } },
    { id: "guard", kind: "guard", at: [330, 520], face: "E", when: (g) => !!g.flag("egypt.shadeSet"),      // on the sunny spot, holding the shade
      life: { still: true, fidget: [6, 14] } },
  ],

  // Make the picture match the story facts. Runs on arrival and after loading a save.
  setup(g) {
    lit(g, "beam-site", g.flag("egypt.shadeSet"));
    if (g.flag("egypt.shadeSet")) redraw(g, "guard", "guard-shade");
  },

  // The far things first: an area lower in this list lies over the ones above it. Each shape follows its thing's own
  // edge, within a few pixels; a thing that is a cut-out or a person says so (`plane`, or an id that is a person's), and
  // Show outlines its own silhouette.
  hotspots: [
    { id: "pyramid", name: "pyramid", poly: [[345, 0], [800, 0], [800, 330], [270, 336], [200, 300], [165, 274], [182, 250]], look: twice("egypt.site.pyramid.look", "egypt.site.pyramid.look2") },
    { id: "small-pyramids", name: "small pyramids", poly: [[6, 281], [37, 228], [59, 272], [87, 240], [101, 264], [115, 264], [130, 239], [143, 263], [143, 281]], look: "egypt.site.small.look" },
    { id: "yard", name: "stone yard", poly: [[29, 293], [44, 288], [78, 280], [100, 276], [150, 275], [166, 284], [166, 296], [150, 305], [128, 306], [96, 316], [57, 317], [28, 316]], look: "egypt.site.yard.look" },
    { id: "scaffold", name: "scaffold", poly: [[634, 99], [648, 95], [655, 62], [718, 58], [745, 108], [772, 163], [800, 205], [800, 383], [772, 386], [742, 372], [716, 262], [682, 252], [662, 196], [640, 156], [640, 108]], look: "egypt.site.scaffold.look" },
    {
      id: "stair", name: "stairs", verb: "Climb", poly: [[686, 400], [746, 400], [659, 269], [613, 269]], walkTo: [742, 424], face: "W",
      look: "egypt.site.stair.look", use: climb, useWith: { pass: climb },
    },
    {
      id: "entrance", name: "entrance", verb: "Climb to", poly: [[497, 188], [541, 143], [587, 188], [570, 192], [567, 268], [516, 268], [512, 192]], walkTo: [742, 424], face: "W",       // the doorway, under its two slabs
      look: (g) => g.say(g.flag("egypt.inside") ? "egypt.site.entrance.look2" : "egypt.site.entrance.look"), use: climb, useWith: { pass: climb },
    },
    { id: "bricks", name: "mud bricks", verb: "Lift", poly: [[507, 373], [589, 374], [591, 384], [617, 385], [636, 390], [636, 398], [592, 397], [507, 386]], walkTo: [560, 410], face: "N", look: "egypt.site.bricks.look", use: liftBrick },      // the bricks drying, and their mold
    { id: "scribe-desk", name: "scribe's station", plane: "awning", poly: [[57, 343], [100, 339], [241, 333], [244, 349], [239, 440], [221, 475], [211, 475], [160, 468], [62, 475], [57, 470]], walkTo: [248, 464], face: "W", look: twice("egypt.site.desk.look", "egypt.site.desk.look2") },      // the awning, and the wages and the office under it
    { id: "rope", name: "hauling rope", poly: [[392, 444], [400, 460], [300, 414], [226, 388], [222, 374], [300, 396]], walkTo: [352, 440], face: "NW", look: "egypt.site.rope.look" },
    { id: "sledge", name: "sledge", verb: "Pull", plane: "sledge", poly: [[394, 453], [397, 458], [407, 455], [424, 469], [559, 481], [562, 466], [568, 463], [565, 440], [552, 439], [552, 385], [478, 379], [454, 382], [442, 389], [443, 433], [439, 435], [421, 423], [415, 428], [424, 442], [418, 445], [405, 435], [398, 438], [403, 448]], walkTo: [420, 492], face: "NE", look: twice("egypt.site.sledge.look", "egypt.site.sledge.look2"), use: "egypt.site.sledge.use" },
    { id: "blocks", name: "masons' tools", verb: "Borrow", plane: "front", poly: [[749, 446], [722, 437], [674, 440], [665, 417], [650, 416], [641, 442], [610, 445], [610, 472], [606, 479], [595, 475], [586, 476], [583, 473], [584, 467], [580, 465], [570, 483], [559, 484], [559, 522], [540, 578], [521, 586], [519, 595], [522, 599], [570, 599], [573, 596], [577, 599], [765, 599], [765, 551], [779, 547], [783, 542]], walkTo: [538, 566], face: "E", look: lookAtStone, use: "egypt.site.blocks.use" },      // the casing blocks, the tools on them, a pole and a coil of rope
    {
      id: "sunspot", name: "sunny spot", verb: "Stand in", poly: [[367, 519], [362, 526], [349, 532], [331, 534], [313, 532], [300, 526], [295, 519], [300, 512], [313, 506], [331, 504], [349, 506], [362, 512]], walkTo: [330, 520], face: "E", when: (g) => !g.flag("egypt.shadeSet"),
      look: (g) => g.say(g.flag("egypt.knowsLight") ? "egypt.site.sunspot.look2" : "egypt.site.sunspot.look"), use: "egypt.site.sunspot.use",
      useWith: { shade: tryShade },
    },
    { id: "water", name: "water jars", plane: "front", poly: [[1, 494], [0, 574], [65, 580], [69, 585], [85, 581], [81, 566], [94, 562], [94, 556], [86, 553], [86, 535], [73, 517], [75, 509], [49, 506], [42, 510], [46, 518], [38, 527], [25, 511], [23, 497]], walkTo: [130, 590], face: "W", look: "egypt.site.water.look" },      // the two jars, and the rails in front of them
    {
      id: "track", name: "track to the river", verb: "Walk down", poly: [[108, 548], [152, 538], [178, 566], [182, 600], [104, 600]], walkTo: [130, 590], face: "W",       // the trodden sand past the fence, off the bottom of the picture
      look: "egypt.site.track.look", use: (g) => g.goto("egypt-crash", { spawn: "fromSite" }),
    },
    // the masons on their planks, far up the faces (round twelve; each stands where the painter's water jar is): a look, nothing more
    { id: "mason1", name: "mason", poly: [[398, 98], [418, 98], [420, 154], [396, 154]], look: "egypt.site.masons.look" },
    { id: "mason2", name: "mason", poly: [[250, 183], [264, 183], [265, 208], [249, 208]], look: "egypt.site.masons.look" },
    // the gang: one speaks, one agrees, one eats (one conversation, and each man his own shape)
    { ...HAULERS, id: "hauler3", poly: [[268, 323], [263, 327], [264, 335], [258, 339], [255, 349], [261, 353], [260, 395], [264, 397], [270, 393], [276, 397], [279, 395], [278, 371], [282, 367], [281, 339], [275, 335], [276, 327]] },
    { ...HAULERS, id: "hauler2", poly: [[294, 336], [288, 342], [289, 347], [283, 351], [286, 369], [286, 406], [290, 408], [296, 404], [302, 408], [305, 406], [305, 369], [308, 362], [308, 351], [302, 347], [302, 340]] },
    { ...HAULERS, id: "hauler1", poly: [[320, 333], [314, 337], [314, 347], [310, 350], [306, 381], [307, 385], [313, 389], [314, 410], [310, 413], [310, 416], [313, 418], [319, 417], [324, 420], [330, 416], [331, 373], [341, 368], [342, 363], [327, 346], [328, 338]] },
    {
      id: "overseer", name: "overseer", verb: "Talk to", poly: [[474, 388], [463, 390], [458, 400], [452, 393], [447, 397], [449, 461], [442, 485], [448, 488], [448, 514], [452, 517], [456, 514], [461, 525], [476, 522], [477, 505], [485, 500], [482, 437], [485, 417], [478, 411], [483, 403], [482, 394]], walkTo: [404, 532], face: "E",
      look: "egypt.overseer.look", use: talkToOverseer,
      useWith: { map: "egypt.overseer.map", shade: "egypt.overseer.shade", carmirror: "egypt.overseer.mirror", coppermirror: "egypt.overseer.mirror", rootbeer: "egypt.overseer.rootbeer", chicken: "egypt.chicken.stock" },
    },
    {
      id: "scribe", name: "scribe", verb: "Talk to", poly: [[150, 392], [144, 397], [145, 408], [141, 411], [142, 426], [140, 440], [145, 447], [164, 452], [169, 448], [169, 440], [173, 437], [173, 428], [170, 426], [165, 427], [160, 423], [159, 416], [161, 411], [159, 407], [162, 401], [156, 393]], walkTo: [248, 464], face: "W",
      look: (g) => g.say(g.flag("egypt.penGiven") ? "egypt.scribe.look2" : "egypt.scribe.look"), use: talkToScribe,
      useWith: { reed: giveReed, map: giveMap, rootbeer: "egypt.scribe.rootbeer", shade: "egypt.scribe.shade", pass: "egypt.scribe.pass", chicken: showGeneral("scribe", "egypt.scribe.chicken") },
    },
    {
      id: "guard", name: "guard", verb: "Talk to", poly: [[669, 324], [664, 361], [666, 420], [673, 419], [672, 370], [677, 368], [681, 394], [677, 419], [693, 424], [699, 420], [701, 380], [697, 340], [689, 333], [684, 335], [678, 357], [673, 358]], walkTo: [742, 424], face: "W", when: (g) => !g.flag("egypt.shadeSet"),
      look: "egypt.guard.look", use: talkToGuard,
      useWith: {
        pass: (g) => (g.flag("egypt.inside") ? g.say("egypt.guard.after") : showPass(g)),
        shade: askGuard, rootbeer: giveRootbeer, sunglasses: "egypt.guard.sunglasses", map: "egypt.guard.map",
        chicken: showGeneral("guard", "egypt.guard.chicken", "egypt.guard.chicken.2"),
      },
    },
    {
      id: "guard-sun", name: "guard", verb: "Talk to", poly: [[440, 372], [392, 395], [368, 400], [357, 409], [351, 407], [341, 416], [340, 391], [332, 385], [319, 390], [320, 520], [339, 523], [345, 476], [342, 445], [363, 429], [425, 407], [444, 390]], walkTo: [268, 534], face: "E", when: (g) => !!g.flag("egypt.shadeSet"),      // the man, and the shade held up in his hands
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

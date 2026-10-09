// Act Two, the first of three scenes: the steps of the temple of Saturn, in the Forum.
// Rome, the morning of the Ides of March, 44 B.C. The Son plays.
//
// The door in time let him out inside the temple and shut behind him, and the doorkeeper has
// carried him out. The door is still in there. To get back to it he has to be what the
// doorkeeper lets in: a boy, in a clean tunic, carrying something for the god.
//
//   chain A   the washerwoman's errand (rome-street): bring the senator, down here, his clean toga.
//             She lends a tunic for it.
//   chain B   the snack-bar keeper's errand (rome-street): bring the soothsayer, on these steps, his
//             breakfast. His sacred chickens feed on the crumbs, the omen is good, and he trusts the
//             boy with the incense he cannot carry up fourteen steps himself.
//   the gate  in the tunic, with the incense, the doorkeeper lets him in (to rome-temple).
//
// And the chickens (briefs/DATING.md: chickens know a door in time before any person does). This morning the sacred
// birds will not touch their grain, which the soothsayer takes for the worst of omens, and they all stand facing the
// temple doors. The boy notices that himself at the cage, and thinks of his little sister. Nobody explains it.
//
// Try it: index.html?scene=rome-steps&lead=son
// Later states: &flags=rome.arrived,rome.knowsRule,rome.hasToga,rome.hasBreakfast   (the things themselves are
// handed over by the people in rome-street, so start there to carry them).

const art = "art/scenes/rome-steps/";

// The painter's frames for the birds (layout.json, "frames"), by number: with `set`, 4 is "<set>-4.png" (briefs/out/fx-4-ready.md).
/** A pigeon: 1 stand, 2 look back, 3 alert, 4-5 peck, 6-9 walk, 10 turn, 11-12 take off, 13-15 fly, 17 glide, 18 land; a soft
    shadow under it on the ground. The right size at row 590, smaller farther off, as people are. */
const PIGEON = (set, more = {}) => ({ set, foot: [23, 40], face: "E", sizeAt: 590, stand: [1, 3], look: [2], peck: [4, 5], walk: [6, 7, 8, 9], turn: [10],
  takeoff: [11, 12], fly: [13, 14, 15], glide: [17], land: [18], shadow: "pigeon-shadow-1.png", ...more });
/** A hen in the cage, seen from behind: standing (now and then a look right, head up, a ruffle), a look left, a shuffle. */
const HEN = (set) => ({ set, foot: [8, 17], face: "E", stand: [1, 3, 1, 4, 1, 7], look: [2], walk: [5, 6] });
const SWALLOW = { flap: ["swallow-1.png", "swallow-2.png", "swallow-3.png", "swallow-2.png"], glide: "swallow-4.png", middle: [8, 5] };
/** The open pavement right of the altar, off the altar, the tripod and the steps: where the pigeons potter. */
const PAVEMENT = [[430, 466], [560, 457], [680, 447], [796, 438], [796, 586], [258, 586], [252, 532], [346, 520], [410, 503]];

/** Has this line been spoken yet? (The engine counts every line it says.) */
const heard = (g, id) => !!g.store.data.seenLines[id];
/** A thing worth looking at twice: the first line the first time, the second after that. */
const twice = (first, second) => (g) => g.say(heard(g, first) ? second : first);
/** Someone who can stand turns to the boy. */
const turnTo = (g, who) => { const a = g.actor(who), me = g.lead; if (a && me) a.look(me.x, me.y); };

// ---------- the pigeons ----------
// Since round four the pigeons are the engine's (`fx`, below: the flocks on the pavement and the two by the cart): they
// potter about, peck, and go up when somebody comes near. Every one of them in the picture is a thing to click, and all
// say the same. Their areas go with them: a few times a second each area is put round one of the birds, as it is drawn
// now, a few pixels outside it (the first area round the first bird there is, and so on), and Show outlines the bird
// itself; an area with no bird left for it (they have flown off over the roofs) is put away until one comes back. With
// no moving things at all (?nofx in the page address) the areas stay where the painted pigeons stood.
const FLOCKS = ["pigeons", "pigeons-dark", "pigeons-pale", "pigeons-left"];
/** Where the painted pigeons stood (their feet): the areas' own places, before the birds are on the stage. */
const PAINTED = [[552, 512], [585, 524], [618, 506], [636, 540], [598, 552], [540, 470], [752, 530], [436, 566], [238, 470], [212, 478]];
const around = ([x, y]) => [[x - 12, y - 15], [x + 12, y - 15], [x + 12, y + 3], [x - 12, y + 3]];

/** "Chase": he says he is not chasing them, and does a little, and up they all go. */
async function chase(g, at = null) {
  const me = g.lead;
  if (me && at) {                                                 // one quick step at them
    const dx = at[0] - me.x, dy = at[1] - me.y, d = Math.hypot(dx, dy) || 1, step = Math.min(24, d * 0.5);
    me.look(at[0], at[1]);
    await g.walkTo(me.x + (dx / d) * step, me.y + (dy / d) * step);
  }
  for (const id of FLOCKS) { const flock = g.effects && g.effects.get(id); if (flock && flock.scare) flock.scare(at || (me ? [me.x, me.y] : null), 260); }
  await g.say("rome.pigeons.use");
}

/** Every pigeon on the pavement is a thing to click on, and all say the same. */
const pigeons = { name: "pigeons", verb: "Chase", look: "rome.pigeons.look", use: (g) => chase(g) };

/** Where a pigeon is painted in its frames (46 by 50, its feet at 23, 40: layout.json), from its feet: 15 to the left or
    right of them whichever way it faces, 17 above them on the ground (in flight its wings go 28 above), 2 below. */
const BIRD_BOX = { half: 16, up: 18, flying: 29, down: 3 };
/** The pigeons' areas go with them (see above). Called a few times a second, on the game's clock. */
function movePigeonAreas(g) {
  const view = g.view, cast = view && view.cast;
  if (!cast || !cast.get("fx:pigeons:0")) return;                // (no moving things: the areas stay where they are)
  const birds = [];
  for (const flock of FLOCKS) for (let n = 0; ; n++) {
    const b = cast.get(`fx:${flock}:${n}`);
    if (!b) break;
    const pic = !b.hidden && b.picture ? b.picture(cast.palette, cast.calm) : null;
    if (!pic || !pic.canvas) continue;
    // the box round the bird as it is drawn now: its size from its picture's (a frame is 46 wide), its feet where they are
    const k = pic.canvas.width / 46, alt = b.alt || 0, x = b.x, y = b.y - alt, B = BIRD_BOX, pad = 2;
    const left = x - B.half * k - pad, right = x + B.half * k + pad, top = y - (alt > 0.5 ? B.flying : B.up) * k - pad, bottom = y + B.down * k + pad;
    if (right < 6 || left > 794 || bottom < 6 || top > 594) continue;          // (flying off over the roofs, out of the picture)
    birds.push({ id: b.id, at: [b.x, b.y], poly: [[left, top], [right, top], [right, bottom], [left, bottom]].map(([px, py]) => [Math.round(px), Math.round(py)]) });
  }
  let k = 0, moved = false;
  view.spots.forEach((spot, i) => {
    if (!spot.pigeon) return;
    let s = spot;
    if (!s.follows) s = view.spots[i] = { ...spot, follows: true };   // (the scene's own area is left as it is)
    const bird = birds[k++], el = view.hotEl.querySelector(`.spot[data-i="${i}"]`);
    if (!bird) {                                                  // no bird for it now: put away until one comes back
      if (!s.away) { s.away = true; s.when = () => false; if (el) el.style.display = "none"; moved = true; }
      return;
    }
    if (s.away) { s.away = false; s.when = undefined; if (el) el.style.display = ""; moved = true; }
    s.plane = bird.id;                                            // (Show outlines the bird itself)
    s.use = (g) => chase(g, bird.at);
    if (s.poly && s.poly.every((p, j) => p[0] === bird.poly[j][0] && p[1] === bird.poly[j][1])) return;
    s.poly = bird.poly;
    view.reshape(i);
    moved = true;
  });
  if (moved && g.outlines && g.outlines.on) g.outlines.changed();
}

/** Something on the stage that draws nothing, and moves the pigeons' areas on the game's clock while the scene is up. */
function followPigeons(g) {
  const cast = g.view && g.view.cast;
  if (!cast || !cast.addPicture || cast.get("pigeon-areas")) return;
  const s = cast.addPicture("pigeon-areas", {}, 0, 0, 1);
  s.picture = () => null;
  let wait = 0;
  s.tick = (dt) => { if ((wait -= dt) <= 0) { wait = 100; movePigeonAreas(g); } };
}

// ---------- the doorkeeper, and the gate ----------

/** He says what he would let in. This is the puzzle stated: everything else in the act serves it.
    A boy who has run an errand or two before asking is scored on what he is carrying. */
async function explainRule(g) {
  turnTo(g, "doorkeeper");
  await g.say("rome.doorkeeper.hi.1", "rome.doorkeeper.hi.2", "rome.doorkeeper.hi.3", "rome.doorkeeper.rule.1", "rome.doorkeeper.rule.2");
  g.flag("rome.knowsRule", true);
  const tunic = g.has("tunic"), gift = g.has("incense");
  if (tunic && gift) return letIn(g);
  await g.say(tunic ? "rome.doorkeeper.need.gift.1" : gift ? "rome.doorkeeper.need.tunic.1" : "rome.doorkeeper.rule.3", "rome.doorkeeper.rule.4");
}

/** The gate of chains A and B. */
async function letIn(g) {
  turnTo(g, "doorkeeper");
  await g.say("rome.gate.1");
  await g.reach();                                                // the tunic goes on over everything (see the note in PUZZLES-rome.md)
  await g.say("rome.gate.2", "rome.gate.3", "rome.gate.4", "rome.gate.5", "rome.gate.6", "rome.gate.7", "rome.gate.8");
  g.flag("rome.inside", true);
  await g.goto("rome-temple");
}

/** Trying the doors, or showing the doorkeeper the tunic or the incense. */
async function atTheDoors(g) {
  if (g.flag("rome.inside")) {                                    // he has been let in once: after that he is known
    if (!heard(g, "rome.doorkeeper.again")) await g.say("rome.doorkeeper.again");
    return g.goto("rome-temple");
  }
  if (!g.flag("rome.knowsRule")) return explainRule(g);
  const tunic = g.has("tunic"), gift = g.has("incense");
  if (tunic && gift) return letIn(g);
  turnTo(g, "doorkeeper");
  if (tunic) return g.say("rome.doorkeeper.need.gift.1", "rome.doorkeeper.need.gift.2");
  if (gift) return g.say("rome.doorkeeper.need.tunic.1", "rome.doorkeeper.need.tunic.2");
  return g.say("rome.doorkeeper.need.both");
}

async function talkToDoorkeeper(g) {
  if (!g.flag("rome.knowsRule")) {
    await explainRule(g);                                         // the rule first; then whatever else there is to say
    if (g.flag("rome.inside")) return;                            // (he met it already, and was let in on the spot)
  } else if (!g.flag("rome.inside") && g.has("tunic") && g.has("incense")) return letIn(g);
  turnTo(g, "doorkeeper");
  for (;;) {
    const pick = await g.choose([
      { id: "rule", line: "rome.doorkeeper.ask.rule", when: (g) => !g.flag("rome.inside") },
      { id: "what", line: "rome.doorkeeper.ask.what" },
      { id: "dad", line: "rome.doorkeeper.ask.dad" },
      { id: "bye", line: "rome.doorkeeper.ask.bye" },
    ]);
    if (pick === "rule") await g.say("rome.doorkeeper.ask.rule", "rome.doorkeeper.ans.rule");
    else if (pick === "what") await g.say("rome.doorkeeper.ask.what", "rome.doorkeeper.ans.what.1", "rome.doorkeeper.ans.what.2");
    else if (pick === "dad") await g.say("rome.doorkeeper.ask.dad", "rome.doorkeeper.ans.dad.1", "rome.doorkeeper.ans.dad.2", "rome.doorkeeper.ans.dad.3", "rome.doorkeeper.ans.dad.4");
    else return g.say("rome.doorkeeper.ask.bye", "rome.doorkeeper.ans.bye");
  }
}

// ---------- chain B ends here: the soothsayer ----------

async function meetSoothsayer(g) {
  if (g.flag("rome.metSoothsayer")) return;
  await g.say("rome.soothsayer.hi.1", "rome.soothsayer.hi.2", "rome.soothsayer.hi.3", "rome.soothsayer.hi.4", "rome.soothsayer.hi.5");
  g.flag("rome.metSoothsayer", true);
}

/** His breakfast arrives. The crumbs go to the sacred chickens, they feed, and that is a good omen:
    now he will send his incense in to the god, by the boy. */
async function feedSoothsayer(g) {
  await meetSoothsayer(g);
  await g.say("rome.soothsayer.fed.1");
  await g.reach();
  g.take("breakfast");
  await g.say("rome.soothsayer.fed.2", "rome.soothsayer.fed.3", "rome.soothsayer.fed.4", "rome.soothsayer.fed.5");
  await g.reach();
  g.give("incense");
  g.flag("rome.hasIncense", true);
  await g.say("rome.soothsayer.fed.6");
}

async function talkToSoothsayer(g) {
  await meetSoothsayer(g);
  for (;;) {
    const fed = !!g.flag("rome.hasIncense");
    const pick = await g.choose([
      { id: "feed", line: "rome.soothsayer.fed.1", when: (g) => g.has("breakfast") },
      { id: "birds", line: "rome.soothsayer.ask.birds" },
      { id: "temple", line: "rome.soothsayer.ask.temple" },
      { id: "future", line: "rome.soothsayer.ask.future" },
      { id: "bye", line: "rome.soothsayer.ask.bye" },
    ]);
    if (pick === "feed") return feedSoothsayer(g);
    if (pick === "birds") {
      if (fed) await g.say("rome.soothsayer.ask.birds", "rome.soothsayer.ans.birds.fed");
      else await g.say("rome.soothsayer.ask.birds", "rome.soothsayer.ans.birds.1", "rome.soothsayer.ans.birds.omen", "rome.soothsayer.ans.birds.2", "rome.soothsayer.ans.birds.3", "rome.soothsayer.ans.birds.4");
    } else if (pick === "temple") {
      if (fed) await g.say("rome.soothsayer.ask.temple", "rome.soothsayer.ans.temple.fed");
      else await g.say("rome.soothsayer.ask.temple", "rome.soothsayer.ans.temple.1", "rome.soothsayer.ans.temple.2", "rome.soothsayer.ans.temple.3", "rome.soothsayer.ans.temple.4");
    } else if (pick === "future") {
      await g.say("rome.soothsayer.ask.future", "rome.soothsayer.ans.future.1", "rome.soothsayer.ans.future.2", "rome.soothsayer.ans.future.3", "rome.soothsayer.ans.future.4");
    } else return g.say("rome.soothsayer.ask.bye", "rome.soothsayer.ans.bye");
  }
}

// ---------- the sacred chickens ----------
// Whether or not they have fed, they all stand facing the temple doors, where the door in time is. The boy notices
// it the first time he calls them, or the second time he looks (whichever comes first), and only once. He looks up
// the steps where they are looking, and thinks of his little sister. He does not explain it, and nobody else does.

/** What he says at the cage; and, once, what he notices there. */
async function atTheCage(g, line, notice) {
  await g.say(line);
  if (!notice || heard(g, "rome.birdcage.doors.1")) return;
  const me = g.lead;
  if (me) me.look(503, 292);                                      // up the steps to the doors, the way they are all facing
  await g.say("rome.birdcage.doors.1");
  if (me) me.face("S");                                           // and round to us: he is thinking of home
  await g.say("rome.birdcage.doors.2");
}

// ---------- chain A, the middle step: the senator ----------

async function meetSenator(g) {
  if (g.flag("rome.metSenator")) return;
  const senator = g.actor("senator");
  await g.moveTo(168, 508, "senator");                            // he is pacing: a few steps away,
  await g.moveTo(200, 540, "senator");                            //        and back to his mark
  if (senator) senator.face("E");
  await g.say("rome.senator.hi.1", "rome.senator.hi.2", "rome.senator.hi.3", "rome.senator.hi.4", "rome.senator.hi.5");
  g.flag("rome.metSenator", true);
}

/** The toga arrives, and the senator leaves for the Senate. (He is not on the steps again: see `actors`.) */
async function deliverToga(g) {
  await meetSenator(g);
  const senator = g.actor("senator");
  await g.say("rome.senator.toga.1");
  await g.reach();
  g.take("toga");
  await g.say("rome.senator.toga.2", "rome.senator.toga.3", "rome.senator.toga.4", "rome.senator.toga.5");
  g.flag("rome.delivered", true);
  await g.moveTo(-50, 468, "senator");                            // off the left edge of the picture, behind the laurel, the way the street goes
  if (senator) senator.fade(0);
  await g.say("rome.senator.toga.6");
}

async function talkToSenator(g) {
  await meetSenator(g);
  for (;;) {
    const pick = await g.choose([
      { id: "give", line: "rome.senator.toga.1", when: (g) => g.has("toga") },
      { id: "late", line: "rome.senator.ask.late" },
      { id: "toga", line: "rome.senator.ask.toga" },
      // Once he has heard whose nose is on the new money (the keeper cries it, the first time he walks into the street),
      // he can ask about Caesar. The senator's gossip is of a great-nephew nobody thinks about: the Caesar Augustus of
      // Luke 2:1, as the boy does not know and nobody in Rome could. It gives nothing and changes nothing.
      { id: "caesar", line: "rome.senator.ask.caesar", when: (g) => g.flag("rome.knowsBC") },
      { id: "dad", line: "rome.senator.ask.dad" },
      { id: "bye", line: "rome.senator.ask.bye" },
    ]);
    if (pick === "give") return deliverToga(g);
    if (pick === "late") await g.say("rome.senator.ask.late", "rome.senator.ans.late.1", "rome.senator.ans.late.2", "rome.senator.ans.late.3", "rome.senator.ans.late.4");
    else if (pick === "toga") await g.say("rome.senator.ask.toga", "rome.senator.ans.toga.1", "rome.senator.ans.toga.2", "rome.senator.ans.toga.3", "rome.senator.ans.toga.4");
    else if (pick === "caesar") await g.say("rome.senator.ask.caesar", "rome.senator.ans.caesar.1", "rome.senator.ans.caesar.2", "rome.senator.ans.caesar.3", "rome.senator.ans.caesar.4", "rome.senator.ans.caesar.5");
    else if (pick === "dad") await g.say("rome.senator.ask.dad", "rome.senator.ans.dad.1", "rome.senator.ans.dad.2");
    else return g.say("rome.senator.ask.bye", "rome.senator.ans.bye");
  }
}

export default {
  id: "rome-steps",
  era: "rome",
  name: "The steps of the temple of Saturn",

  // WHERE THINGS ARE. Every place in this file is the painter's own measurement of the finished picture
  // (art/scenes/rome-steps/layout.json), or was set by eye against the picture with the people standing in it.
  // The act's check script (check-rome.mjs) reads this file against that one; the few differences that are meant are listed there.
  // (The painter moved several things from where briefs/SCENES.md has them: the porch is at row 298, the doors at 468
  // to 538, the soothsayer sits on the fourth step, and the way to the street is off the left edge of the pavement.)

  // DEPTH. The pavement is ordinary ground. The steps are not: they climb the picture faster than the ground does.
  // minScale is the painter's: people hold the size they have at row 392 from there upward, instead of shrinking
  // away toward the horizon as they climb.
  horizon: 260, full: 590, minScale: 0.4,

  // The pavement, the whole flight of steps, and the narrow strip of porch behind the columns.
  walk: { area: [[0, 597], [797, 597], [797, 433], [797, 298], [763, 298], [648, 291], [342, 296], [396, 305], [382, 306], [461, 461], [400, 462], [340, 452], [240, 446], [120, 442], [0, 438]] },
  // Ground that things stand on. (A cut-out can block one patch of its own; the columns need six, so they are all here.)
  blocked: [
    [[238, 521], [346, 510], [327, 487], [229, 496]],             // the altar
    [[366, 498], [404, 495], [393, 485], [357, 489]],             // the tripod
    [[672, 563], [746, 553], [710, 535], [639, 544]],             // the boundary stone
    [[448, 422], [505, 419], [489, 403], [434, 406]],             // the soothsayer's cage
    [[0, 500], [150, 484], [158, 600], [0, 600]],                 // the statue base at the bottom left (the front plane)
    [[340, 306], [389, 306], [375, 303], [328, 304]],             // the feet of the six columns
    [[441, 305], [486, 304], [468, 301], [425, 302]],
    [[535, 303], [577, 302], [554, 300], [514, 301]],
    [[622, 301], [660, 301], [634, 298], [597, 299]],
    [[702, 300], [738, 299], [709, 297], [674, 298]],
    [[777, 298], [811, 298], [779, 296], [747, 297]],
    [[556, 293], [595, 293], [586, 292], [547, 292]],             // the doorkeeper's bench
  ],
  spawn: {
    default: [470, 508],                                          // the foot of the steps: where the doorkeeper put him down
    fromStreet: [52, 472],                                        // coming in from the street, at the left edge, behind the laurel (see `enter`)
    fromTemple: [517, 295],                                       // coming out of the doors (the same place as the doors' walkTo, below)
  },
  exits: ["rome-street", "rome-temple"],
  // The way out across the edge of the picture (round three): the street is off the left edge, behind the laurel, so a
  // click anywhere down the left side, where there is nothing else, walks him to the painter's way out and on into the
  // street, as the way out there does ("to-street", below). The temple's doors are in the middle of its front wall: they
  // stay a thing to click on, and are not an edge.
  edges: {
    W: { to: "rome-street", spawn: "fromForum", name: "to the street", walkTo: [34, 470] },
  },

  picture: art + "back.png",
  planes: [
    { id: "columns", src: art + "columns.png", base: [[320, 305.3], [800, 296.8]] },   // the six columns of the front: people on the porch pass behind them
    { id: "altar", src: art + "altar.png", base: [[244, 518], [338, 509]] },
    { id: "tripod", src: art + "tripod.png", base: 495 },
    { id: "stone", src: art + "stone.png", base: [[673, 558], [730, 550]] },
    // The front of the hens' cage, cut from the picture itself (laid over it, it changes nothing): the hens stand behind
    // its bars, and the soothsayer, on the step below, in front of it.
    { id: "cage-front", src: art + "cage-front.png", base: [[445, 409], [477, 407]] },
    // The statue base and the laurel at the bottom left corner, in two, so that the laurel's branch can stir (together
    // they are front.png, pixel for pixel).
    { id: "front", src: art + "front-base.png", plane: "front" },
    { id: "laurel", src: art + "laurel.png", plane: "front" },
  ],

  // THINGS THAT MOVE BY NATURE (round four: briefs/out/paint-4a-ready.md). Nothing that moves is painted still: the
  // painter took them out of the picture and marked where they go (layout.json, "fx"), and the engine draws them moving.
  fx: [
    // the wisp from the pan of embers on the altar, leaning left with the morning air (the one the author saw), and the coals
    { id: "altar-smoke", type: "smoke", at: [286, 429], base: [[244, 518], [338, 509]], height: 196, width: [2, 15], lean: [-30, -196], rise: 20, rate: 2.5, gust: 0.3, color: "#f6efe2", opacity: 0.45 },
    { id: "altar-embers", type: "embers", at: [286, 430], base: [[244, 518], [338, 509]], size: [13, 2.5], count: 9, sparks: 0.15 },
    // a sacrifice's smoke far off on the Capitol
    { id: "hill-smoke", type: "smoke", plane: "back", at: [151, 190], height: 62, width: [1, 7], lean: [-15, -62], rise: 7, rate: 2, gust: 0.2, color: "#f4ecde", opacity: 0.35 },
    // pigeons on the pavement, in three colours, and two by the cart's shade: each sorts by its own feet, and shrinks with
    // depth as people do. They are things to click (see the top of the file).
    { id: "pigeons", type: "birds", kind: "flock", area: PAVEMENT, count: 5, frames: PIGEON("pigeon") },
    { id: "pigeons-dark", type: "birds", kind: "flock", area: PAVEMENT, count: 2, frames: PIGEON("pigeon-dark"), seed: 2 },
    { id: "pigeons-pale", type: "birds", kind: "flock", area: PAVEMENT, count: 1, frames: PIGEON("pigeon-pale"), seed: 3 },
    { id: "pigeons-left", type: "birds", kind: "flock", area: [[150, 458], [228, 450], [234, 486], [156, 492]], count: 2, frames: PIGEON("pigeon") },
    // three on the right-hand end of the steps, keeping to the treads (measured at the middle of their stretch)
    { id: "pigeons-steps", type: "birds", kind: "flock", area: [[665, 432], [796, 422], [796, 355], [618, 363]], count: 3, frames: PIGEON("pigeon", { sizeAt: undefined }), depth: false, scale: 0.52, treads: [424, 411, 399, 388, 377, 367, 357] },
    // four along the temple's gutter, high up, out of anyone's reach: now and then one flies off and comes back
    { id: "pigeons-gutter", type: "birds", kind: "flock", plane: "back", perch: [[644.7, 15.1], [760.7, 27.9]], count: 4, frames: PIGEON("pigeon", { sizeAt: undefined, shadow: undefined }), scale: 0.32, shy: 0, moves: { stand: 4, look: 2, peck: 0.5, walk: 1, turn: 1, away: 0.15 } },
    // swallows over the square, back for the spring (only in the open sky left of the temple)
    { id: "swallows", type: "birds", kind: "flyers", plane: "back", lanes: [[[-12, 118], [90, 94], [180, 66], [244, 30], [262, -12]], [[-12, 64], [70, 44], [150, 26], [232, -12]]], frames: SWALLOW, scale: 1, every: [6, 14], group: [1, 2], speed: 120 },
    { id: "swallows-far", type: "birds", kind: "flyers", plane: "back", lanes: [[[250, -12], [170, 40], [80, 88], [-12, 150]], [[-12, 132], [60, 112], [140, 100], [236, 70], [262, -12]]], frames: SWALLOW, scale: 0.55, every: [7, 16], group: [1, 3], speed: 80 },
    // the laurel's branch at the front stirring
    { id: "laurel-sway", type: "sway", plane: "laurel", anchor: "top", amount: 1.2, period: 4.2, wave: 70, lean: 0.2 },
    // the soothsayer's two hens in the cage, behind its bars (cage-front): they never peck, turn round or fly, and always
    // face the temple doors (they refuse their grain, and face the doors even after they have fed)
    { id: "hen-white", type: "birds", kind: "flock", area: [[454.5, 404.6], [457.5, 404.6], [457.5, 406.6], [454.5, 406.6]], count: 1, frames: HEN("hen-white"), shy: 0, fly: false, turn: false, depth: false, walk: 3, moves: { stand: 3, look: 2, walk: 1, peck: 0, turn: 0 } },
    { id: "hen-brown", type: "birds", kind: "flock", area: [[466.8, 404.6], [469.8, 404.6], [469.8, 406.6], [466.8, 406.6]], count: 1, frames: HEN("hen-brown"), shy: 0, fly: false, turn: false, depth: false, walk: 3, moves: { stand: 3, look: 2, walk: 1, peck: 0, turn: 0 } },
  ],

  actors: [
    // He is seen between the second and third columns, beside the doorway. The porch is a strip fourteen rows deep and the
    // columns' feet take most of it, so he blocks no ground: the one gap wide enough to come up through is where he stands.
    { id: "doorkeeper", kind: "doorkeeper", at: [492, 295], face: "S", solid: false, life: { still: true, fidget: [6, 14] } },     // (he keeps the door: small movements only)
    // He sits on the fourth step, beside his cage, with his feet on the third. The painter's mark (494, 404) is his seat;
    // a seated figure's place is the ground under its hips, which is one step (ten rows) straight down from the seat.
    { id: "soothsayer", kind: "soothsayer", at: [505, 414], face: "S",
      life: { every: [30, 55], spots: [[468, 436, "N"], [550, 402, "N"]], stay: [4, 8] } },       // up off his step: round to the front of his cage to look at his birds, or along the step
    // He paces, and in the end he walks away, so he blocks no ground. Once his toga has come he is gone.
    { id: "senator", kind: "senator", at: [200, 540], face: "E", solid: false, when: (g) => !g.flag("rome.delivered"),
      life: { every: [10, 20], spots: [[180, 506, "N"], [244, 560, "E"]], stay: [1.5, 3] } },     // pacing: a few steps off and back
  ],

  // Back to front: a later area lies over an earlier one.
  // SHAPES (round three: the Show button outlines each thing, so each shape hugs its thing, a few pixels outside its edge).
  // They were traced from the painter's picture and cut-outs, and the people from the figures the engine draws at their
  // marks. A thing that is a painted cut-out names it (`plane`): Show then outlines the cut-out's own edge. The temple and
  // the far right of the flight were traced from the picture before, and were already tight. The five pigeons by the
  // puddle are five things to click, and all say the same.
  hotspots: [
    { id: "forum", name: "Forum", poly: [[0, 212], [14, 186], [22, 174], [31, 175], [34, 195], [54, 187], [55, 144], [97, 118], [101, 118], [137, 143], [138, 181], [152, 182], [158, 186], [200, 201], [238, 209], [240, 288], [236, 304], [0, 304]], walkTo: [140, 470], face: "N", look: twice("rome.forum.look", "rome.forum.look2") },      // the hill and its great temple, against the sky, and the Forum below it
    // The temple itself, traced from the picture: the side wall, the six columns and everything above them.
    { id: "temple", name: "temple", verb: "Climb", poly: [[240, 96], [345, 0], [800, 0], [800, 292], [326, 292], [244, 286]], look: "rome.temple.look", use: "rome.temple.use" },
    { id: "stairs", name: "temple steps", poly: [[700, 306], [797, 306], [797, 430], [700, 440]], look: "rome.stairs.look" },      // the far right of the flight: the rest is for walking on
    // Two things the painter put in the shade of the temple's base, which are not in the painter's list: traced from the picture.
    { id: "cart", name: "handcart", poly: [[146, 362], [180, 342], [183, 336], [190, 326], [200, 320], [214, 321], [222, 327], [228, 336], [231, 343], [248, 350], [262, 352], [262, 312], [273, 312], [273, 368], [262, 374], [236, 374], [226, 368], [220, 364], [206, 366], [196, 360], [150, 368]], walkTo: [196, 454], face: "N", look: "rome.cart.look" },      // the cart, its sealed sacks, and the low door of the vault they have come for
    {
      id: "dog", name: "sleeping dog", verb: "Call", poly: [[206, 384], [211, 378], [216, 381], [222, 380], [232, 380], [244, 381], [251, 384], [256, 388], [254, 393], [206, 393]], walkTo: [232, 456], face: "N",
      look: "rome.dog.look", use: "rome.dog.use", useWith: { breakfast: "rome.dog.breakfast" },
    },
    {
      // The painter's place to stand is 517, 296. One row up from it is clear of the margin the engine keeps round the third column's foot.
      // (The door leaves and the dark between them, and the garland over them.)
      id: "doors", name: "temple doors", verb: "Go through", poly: [[470, 133], [535, 133], [535, 151], [532, 153], [532, 294], [473, 294], [473, 152], [470, 150]], walkTo: [517, 295], face: "N",
      look: (g) => g.say(g.flag("rome.inside") ? "rome.doors.look2" : "rome.doors.look"),
      use: atTheDoors, useWith: { tunic: atTheDoors, incense: atTheDoors },
    },
    { id: "notices", name: "notice board", poly: [[340, 327], [355, 317], [370, 327], [370, 374], [340, 374]], walkTo: [425, 472], face: "N", look: "rome.board.look" },      // the board, and the cord it hangs by
    {
      id: "altar", name: "altar", verb: "Touch", plane: "altar", poly: [[320, 413], [314, 410], [308, 412], [305, 416], [306, 424], [301, 422], [283, 424], [280, 422], [276, 425], [259, 427], [249, 415], [243, 415], [239, 418], [239, 442], [243, 448], [243, 478], [239, 480], [239, 485], [234, 487], [234, 499], [242, 518], [252, 519], [339, 509], [339, 498], [335, 485], [329, 483], [329, 475], [332, 473], [329, 458], [334, 451], [335, 428]], walkTo: [309, 529], face: "N",
      look: "rome.altar.look", use: "rome.altar.use", useWith: { incense: "rome.altar.incense" },
    },
    { id: "tripod", name: "bronze tripod", plane: "tripod", poly: [[363, 406], [358, 408], [354, 413], [356, 419], [361, 419], [367, 424], [363, 451], [363, 484], [361, 491], [371, 491], [369, 485], [370, 461], [375, 460], [379, 462], [378, 495], [386, 496], [388, 495], [388, 490], [394, 489], [392, 482], [390, 424], [397, 419], [402, 419], [404, 412], [400, 408], [390, 405]], walkTo: [431, 494], face: "W", look: "rome.tripod.look" },
    // (The painter's place to stand for the stone is 624, 568, where the inventory bar would hide his feet: he stands a little higher.)
    { id: "stone", name: "carved stone", plane: "stone", poly: [[654, 475], [652, 478], [652, 548], [672, 559], [728, 552], [731, 550], [731, 481], [728, 477], [696, 465], [672, 466]], walkTo: [618, 540], face: "E", look: "rome.stone.look" },
    // The ten pigeons on the pavement (round four: the engine's, and their areas go with them: see the top of the file).
    // These shapes are where the painted ones stood, for the moment before the birds are on the stage.
    ...PAINTED.map((at, n) => ({ id: n ? `pigeons-${n + 1}` : "pigeons", ...pigeons, pigeon: true, poly: around(at) })),
    {
      // The cage and its dish of grain. (What he notices about the birds: see `atTheCage`, above.)
      id: "birdcage", name: "sacred chickens", verb: "Call", poly: [[438, 383], [454, 382], [455, 377], [462, 377], [463, 382], [480, 383], [480, 400], [494, 400], [495, 408], [438, 410]], walkTo: [524, 462], face: "NW",
      look: (g) => {
        const again = heard(g, "rome.birdcage.look") || heard(g, "rome.birdcage.fed");
        return atTheCage(g, g.flag("rome.hasIncense") ? "rome.birdcage.fed" : again ? "rome.birdcage.look2" : "rome.birdcage.look", again);
      },
      use: (g) => atTheCage(g, g.flag("rome.hasIncense") ? "rome.birdcage.fed" : "rome.birdcage.use", true),
      useWith: { breakfast: "rome.birdcage.breakfast" },
    },
    {
      // His figure, with the staff in his hand. He is talked to from beside him, two steps down, so that the boy does not
      // stand in front of the old man.
      id: "soothsayer", name: "soothsayer", verb: "Talk to", poly: [[488, 355], [485, 357], [485, 390], [483, 393], [485, 397], [485, 417], [488, 419], [491, 417], [492, 396], [493, 419], [498, 422], [506, 417], [512, 422], [516, 419], [516, 403], [519, 401], [522, 392], [511, 367], [507, 364], [498, 367], [493, 382], [491, 382], [491, 357]], walkTo: [540, 442], face: "W",
      look: twice("rome.soothsayer.look", "rome.soothsayer.look2"), use: talkToSoothsayer,
      useWith: {
        breakfast: feedSoothsayer,
        toga: "rome.soothsayer.toga",
        coin: ["rome.soothsayer.coin.1", "rome.soothsayer.coin.2", "rome.soothsayer.coin.3"],
        quarter: "rome.soothsayer.quarter", incense: "rome.soothsayer.incense",
      },
    },
    {
      id: "senator", name: "senator", verb: "Talk to", poly: [[197, 401], [188, 407], [189, 420], [180, 444], [180, 452], [184, 459], [183, 515], [184, 527], [193, 531], [193, 543], [208, 545], [213, 541], [213, 534], [209, 531], [214, 528], [214, 465], [216, 461], [219, 462], [223, 459], [222, 454], [225, 451], [234, 454], [237, 450], [229, 440], [217, 438], [210, 423], [210, 419], [213, 417], [210, 408], [204, 402]], walkTo: [264, 540], face: "W",
      when: (g) => !g.flag("rome.delivered"),
      look: twice("rome.senator.look", "rome.senator.look2"), use: talkToSenator,
      useWith: { toga: deliverToga, breakfast: "rome.senator.breakfast", incense: "rome.senator.incense" },
    },
    {
      // He is small up there (68 pixels), and his area is his figure, with the staff he holds. All round him is the
      // doorway, which leads to him too until he has let the boy in (see `atTheDoors`).
      id: "doorkeeper", name: "doorkeeper", verb: "Talk to", poly: [[474, 223], [470, 226], [471, 296], [474, 298], [477, 296], [477, 257], [480, 256], [481, 295], [486, 298], [492, 294], [498, 298], [502, 295], [502, 257], [512, 252], [513, 248], [506, 237], [493, 224], [485, 228], [478, 240], [478, 226]], walkTo: [517, 295], face: "W",
      look: twice("rome.doorkeeper.look", "rome.doorkeeper.look2"), use: talkToDoorkeeper,
      useWith: {
        tunic: atTheDoors, incense: atTheDoors,
        toga: "rome.doorkeeper.toga",
        breakfast: ["rome.doorkeeper.breakfast.1", "rome.doorkeeper.breakfast.2", "rome.doorkeeper.breakfast.3"],
        coin: "rome.doorkeeper.coin", quarter: "rome.doorkeeper.quarter", phone: "rome.doorkeeper.phone",
      },
    },
    {
      // The painter's way out is the left edge of the pavement, 40 pixels wide, behind the laurel. (It used to be wider, to be
      // easier to find. Now the whole left edge of the picture is the way to the street: see `edges`.)
      id: "to-street", name: "the street", verb: "Walk to", poly: [[0, 438], [40, 440], [40, 500], [0, 500]], walkTo: [34, 470],
      look: "rome.tostreet.look", use: (g) => g.goto("rome-street", { spawn: "fromForum" }),
    },
  ],

  // Runs as the scene is built, and after a save is loaded: the pigeons' areas go with the pigeons.
  setup(g) {
    followPigeons(g);
  },

  // Runs when the lead arrives. It must be safe to run twice, so it checks its own fact.
  async enter(g, from) {
    if (from === "rome-street") await g.walkTo(160, 474);         // out from behind the laurel at the left edge, onto the open pavement
    if (g.flag("rome.arrived")) return;
    const me = g.lead, doorkeeper = g.actor("doorkeeper");
    await g.wait(400);
    if (me) me.face("N");
    if (doorkeeper && me) doorkeeper.look(me.x, me.y);
    await g.say("rome.arrive.out");
    if (me) me.face("S");                                         // he turns and sees where he is
    await g.say("rome.arrive.1", "rome.arrive.2");
    if (me) me.face("N");                                         // and back to the temple: the door is in there
    await g.say("rome.arrive.4", "rome.arrive.5", "rome.arrive.3", "rome.arrive.6");
    if (me) me.face("W");                                         // the street is off the left edge, behind the laurel: his nose says so
    await g.say("rome.arrive.7");
    for (const thing of ["phone", "quarter", "gum"]) g.store.give(thing);   // what was in his pockets all along (no "You have..." for these)
    g.flag("rome.arrived", true);
    g.team(["son"]);                                              // he plays this act alone: Dad is still in Egypt, at his door
  },
};

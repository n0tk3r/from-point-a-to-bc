// Act Two: across the Tiber (ROME-13S3: new in round thirteen; briefs/SCENES-13R3.md, the design's 2.4, 5.7 and section 6).
// Rome, the morning of the Ides of March, 44 B.C. The Son plays.
//
// The right bank of the river below the stone bridge, looking downstream: a lane of small houses where a Jewish family lives
// beside their house of prayer, a hen yard, a landing where a barge is being loaded, and the river in the morning sun. The
// quiet place of the act, and the heart of its faith thread (the design's section 6). Three people live here:
//
//   Eleazar   the date seller's father-in-law, an old man of Jerusalem, at his upper window, praying toward Jerusalem. The
//             first time the boy goes to him (or to his door, his window, his bench) he waits until the old man has finished
//             (`waitForHim`); then the old man comes down to his bench and they talk (`eleazarTree`): who he is, Daniel's
//             window, how he came to Rome, what he prays for, and the heart of it, Isaiah 40:31. They pray side by side,
//             facing the river and Jerusalem; and the blessing goes three ways: his hand on the boy's head (Numbers 6:25),
//             and the boy gives him the last part back (Numbers 6:26). The talk gives nothing and needs nothing. The music
//             drops for it, and the river is heard. Slowly, with room round the words, as the date seller's blessing in the
//             street (rome-street.js, `whatHePraysFor`) is staged.
//   Mariam    his granddaughter, about eight, among her hens (`mariamTree`). Her hens stand in a row looking over the river at
//             the city and will not eat: the act's thread of chickens, one more place. Nobody explains it.
//   Felix     Phyllis's son, a boatman, loading the barge (`felixTree`): the middle step of NEW 4, Interest Is Extra Wishes.
//             The boy brings him his mother's lamp, and he gives his word that he will come over the bridge before the barge
//             goes down (rome.felixWord: the hook `lamp`, below). Then he takes up his bale and goes back to work.
//
// The only way out is the bottom edge: back over the stone bridge to the Forum (the bridge is behind us).
//
// Every place below is the painter's own measurement of the finished picture (art/scenes/rome-tiber/layout.json, and
// S/work-rome-paint3/ready.md), or was set by eye against the picture with the people standing in it; where the two
// differ, the comment says why.
//
// Try it: index.html?scene=rome-tiber&lead=son&flags=rome.knowsBC
// Later states: add rome.sawTiber,rome.eleazarDown (he is on his bench); and for Felix, in the console,
// game.give("lamp"); game.flag("rome.hasLamp", true)  (the lamp is Phyllis's, from the Forum).

import { eleazarTree, mariamTree, felixTree } from "../talk/rome.js";
import { scaleAt } from "../../engine/walk.js";
import { BLESS_STEP } from "../../art/people.js";

const art = "art/scenes/rome-tiber/";

/** Has this line been spoken yet? (The engine counts every line it says.) */
const heard = (g, id) => !!g.store.data.seenLines[id];
/** A thing worth looking at twice: the first line the first time, the second after that. */
const twice = (first, second) => (g) => g.say(heard(g, first) ? second : first);
/** Someone who can stand turns to the boy. (Not the old man on his bench: someone sitting stays as he sits.) */
const turnTo = (g, who) => { const a = g.actor(who), me = g.lead; if (a && me) a.look(me.x, me.y); };
/** Has the old man come down from his window? (The wait, or the boy's going away after seeing him at prayer.) */
const down = (g) => !!g.flag("rome.eleazarDown");

// ---------- the marks (layout.json, "marks") ----------
const STEP_IN = [516, 534];            // a step in from the painter's arrival mark (fromBridge, [520, 562]): off the bridge, onto the lane
const WINDOW = [659.9, 286.9];         // marks.window.at: the floor of the upper room under his feet, behind the wall, 40 cm back from it
const WINDOW_SCALE = 0.561;            // marks.window.scale: a grown man standing there, the sill at his waist (the painter's camera)
const OPENING = [[680, 234], [640, 234], [640, 178], [680, 173]];     // marks.window_opening: his area while he is up there
const BENCH = [500, 408];              // marks.bench_seat.at: the ground under his hips on the bench (45 cm: TIBER_BENCH_SEAT)
// He sits facing the lane, and us (the bench's front, seen at the house front's slant); the boy stands at its near end,
// beside him, to talk to him.
const BENCH_FACE = "S";
const DOOR = [573, 427];               // marks.door: before his door, where he comes out
const WAIT = [520, 427];               // marks.wait: beside the bench's near end: where the boy waits, and talks to him
const PRAY_EL = [455, 404];            // marks.pray_eleazar, facing W (the river, and Jerusalem beyond it)
const PRAY_SON = [486, 418];           // marks.pray_son, facing W: beside him, nearer us and a little to one side
const BLESS_AT = [439, 403];           // marks.bless: the old man's place for the blessing, facing E (the boy at BLESS_STEP, east of him)
const ASIDE = [470, 446];              // where the boy steps back to, out of the old man's way, as he comes out of his door
const BACK = [462, 430];               // and a step back from the blessing, to let him by to his bench
const AWAY = [466, 486];               // where the boy walks to after the blessing, a few steps off down the lane, and turns to us
const MARIAM = [646, 474];             // marks.mariam: in the hen yard, behind its fence, facing W with her hens
const MARIAM_TALK = [547, 474];        // marks.mariam_talk: on the lane outside the fence, beside her, the fence between them
const FELIX = [82, 463];               // marks.felix: on the landing, by the pile of bales
// Talking to Felix: on the landing a step east of him, turned to him. (The landing is small on the screen: the painter's
// stands for the bales, the landing and the barge lie close round him; this one is clear of the bollard and of all three.)
const FELIX_TALK = [144, 466];

// ---------- the old man at his window, and the wait ----------
// He stands at his upper window praying: one of the scene's people, his feet on the floor of the upper room behind the wall
// (the cut-out `window-wall`, the opening cut clear), drawn at the window's own scale (docs/DESIGN.md, section 3, "Someone
// above the floor"). His way of standing is his prayer (PEOPLE-13R's `eleazar-window`: stance "prayer", hands folded at his
// breast so that they show over the sill, head bowed); his life plays his only two small movements, `lift` (his head lifted
// a while, his lips moving) and `murmur`. So the scene does not call pray(true) on him: it would stop both, and he would
// look the same. Nothing turns him toward the boy.

/** He comes out of his door on his feet, his scroll in his hand: the same man under the same id, now as PEOPLE-13R's
    `eleazar`, whose seat is the bench (found sitting there, got up at once, and put at his door). */
function comeOut(g) {
  const cast = g.view.cast;
  cast.remove("eleazar");
  const el = cast.addFigure("eleazar", "eleazar", BENCH[0], BENCH[1], scaleAt(g.scene, BENCH[1])).face(BENCH_FACE);
  el.sit(false, true);                                            // up at once: the bench is remembered as his seat
  el.place(DOOR[0], DOOR[1], scaleAt(g.scene, DOOR[1])).face("W");
  el.fade(0);
  el.flag("clear", true);                                         // (see `setup`)
  return el;
}

/** The old man walks, slowly, through the points given, in straight lines. The ground before his door and his bench is his
    own: he keeps a hand's breadth in front of the bench, where the walk map's margin round it would keep him further off. */
async function walkHim(g, points) {
  const el = g.actor("eleazar");
  if (el) await el.walkPath(g.clock, points, (y) => scaleAt(g.scene, y));
}
// His ways: along the front of the bench from his door to his place on it, and back to it from where he prays.
const FROM_DOOR = [[530, 421], [506, 418]];
const FROM_BLESSING = [[470, 409]];

/** Back to his bench (through `via`), and down onto it as he got up. */
async function toHisBench(g, via = []) {
  const el = g.actor("eleazar");
  if (!el || !el.up) return;
  await walkHim(g, [...via, el.standAt]);
  await el.sit(true);
}

/**
 * The wait (the design's 6.2, step 2). The first time the boy goes to the old man at his window (or knocks at his door,
 * or goes to the window or the bench), he does not interrupt: he goes to the bench's near end and waits, facing the house.
 * A short wait on the game clock: the hens, the river, the old man's head lifted at the window. Then the Son's line, to us.
 * The old man finishes, steps back from the window and is gone; a moment (the stairs inside); he comes out of his door
 * with his scroll, walks to his bench and sits; and his talk begins. `first`: what the boy says first (the house: he was
 * going to knock; the bench: he was going to sit).
 */
async function waitForHim(g, first = null) {
  if (down(g)) return talkToEleazar(g);
  const me = g.lead, w = g.actor("eleazar");
  if (first) await g.say(first);
  await g.walkTo(WAIT[0], WAIT[1]);
  if (me) me.look(DOOR[0] + 15, DOOR[1] - 40);                    // facing the house: his door, and his window above it
  await g.wait(1400);
  if (w) w.fidget("lift");                                        // (at the window: his head lifted a while, his lips moving)
  await g.wait(1600);
  if (me) me.face("S");                                           // to us
  await g.say("rome.eleazar.wait");
  if (me) me.look(WINDOW[0], WINDOW[1] - 60);                     // and back up at the window
  await g.wait(1300);
  // He has finished. He steps back from the window, and is gone.
  if (w) { w.fidget(null); await g.tween(500, (k) => w.fade(1 - k)); }
  await g.wait(1100);                                             // (down the stairs inside)
  // Out of his door, on his feet, with his scroll. The boy steps back out of his way, and watches him along to his
  // bench, and down onto it; then comes to stand at its near end, beside him.
  const el = comeOut(g);
  g.flag("rome.eleazarDown", true);
  if (me) me.look(DOOR[0], DOOR[1] - 30);
  await g.tween(350, (k) => el.fade(k));
  await g.wait(300);
  await g.walkTo(ASIDE[0], ASIDE[1]);
  if (me) me.look(el.x, el.y);
  await toHisBench(g, FROM_DOOR);
  await g.wait(400);
  g.remap();                                                      // (he is on his bench: the ground before it is free again)
  await g.walkTo(WAIT[0], WAIT[1]);
  if (me) me.look(el.x, el.y - 20);
  await g.wait(600);
  await talkToEleazar(g);
}

// ---------- his talk (eleazarTree: the hooks are the staging, all of it slow) ----------

/** The boy turns to us for a line that is not for the person he is talking to, and back. */
function aside(g, on, who) {
  const me = g.lead, a = g.actor(who);
  if (!me) return g.wait(0);
  if (on) me.face("S");
  else if (a) me.look(a.x, a.y - 20);
  return g.wait(on ? 450 : 350);
}

/** "Shall we wait together a little?" He gets up, slowly, and goes to stand by the bench facing the river, and Jerusalem
    beyond it; the boy comes to stand beside him, a little nearer us, facing the same way; and both pray. */
async function prayTogether(g) {
  const el = g.actor("eleazar"), me = g.lead;
  if (!el || !me) return;
  await g.wait(500);
  await el.sit(false);                                            // (slowly: he is old)
  await walkHim(g, [PRAY_EL]);
  el.face("W");
  await g.wait(300);
  g.remap();                                                      // (the ground he stood on is free again, and he stands here now)
  await g.walkTo(PRAY_SON[0], PRAY_SON[1]);
  me.face("W");
  await g.wait(700);
  el.pray(true);
  await g.wait(700);
  me.pray(true);                                                  // his head goes down, and his hair stays up
  await g.wait(1200);
}

/** Amen: both lift their heads. */
async function amen(g) {
  const el = g.actor("eleazar"), me = g.lead;
  await g.wait(600);
  if (el) el.pray(false);
  if (me) me.pray(false);
  await g.wait(900);
}

/** "Come. Stand still a moment." He takes a step to his left and turns to the boy; the boy stands before him, on the same
    row, his feet BLESS_STEP of the old man's height in front of the old man's; the boy's head goes down, and the old man's
    hand comes to rest on it. Then he says Numbers 6:25. */
async function bless(g) {
  const el = g.actor("eleazar"), me = g.lead;
  if (!el || !me) return;
  await walkHim(g, [BLESS_AT]);
  el.face("E");
  const at = [BLESS_AT[0] + BLESS_STEP * el.sizeNow(), BLESS_AT[1]];
  await g.moveTo(at[0], at[1]);                                   // (exactly there: the walk map keeps a margin round him that this is inside)
  me.face("W");
  await g.wait(600);
  me.pray(true);
  el.hold(true, "bless");                                         // his right hand, eased down onto the boy's head
  if (el.act) await g.tween(450, (k) => { el.act.k = k; });
  await g.wait(500);
}

/** The hand comes away, and both heads come up. */
async function release(g) {
  const el = g.actor("eleazar"), me = g.lead;
  await g.wait(700);
  if (el && el.act) await g.tween(450, (k) => { el.act.k = 1 - k; });
  if (el) el.hold(false);
  if (me) me.pray(false);
  await g.wait(800);
}

/** "Go in peace, child. And find your father." He goes back to his bench and sits; the music comes back. */
async function rest(g) {
  const me = g.lead, el = g.actor("eleazar");
  g.music(g.musicOf(g.scene));
  await g.wait(400);
  await g.moveTo(BACK[0], BACK[1]);                               // (a step back, out of his way: still facing him)
  if (me && el) me.look(el.x, el.y);
  await toHisBench(g, FROM_BLESSING);
  if (me && el) me.look(el.x, el.y - 20);
  await g.wait(500);
}

/** The boy walks a few steps off down the lane, and turns to us: his last line is ours. */
async function away(g) {
  const me = g.lead;
  await g.walkTo(AWAY[0], AWAY[1]);
  if (me) me.face("S");
  await g.wait(500);
}

const ELEAZAR = eleazarTree({ aside: (g, on) => aside(g, on, "eleazar"), pray: prayTogether, amen, bless, release, rest, away });

/** The talk. While he talks with the boy (from his greeting to his "Go in peace") the music drops and the river is heard;
    it comes back after. (After the blessing there is one line, and the music stays.) */
async function talkToEleazar(g) {
  const me = g.lead, el = g.actor("eleazar");
  if (me && el) me.look(el.x, el.y - 20);
  const quiet = !g.flag("rome.blessed");
  if (quiet) { g.music(null); g.sfx("river"); }
  try {
    await g.talk(ELEAZAR);
  } finally {
    if (quiet) g.music(g.musicOf(g.scene));
    if (el && g.actor("eleazar") === el && el.up) await toHisBench(g, FROM_BLESSING);      // (a talk that ended with him on his feet: back to his bench)
  }
}

// ---------- Mariam, and her hens ----------

/** She crouches to look a hen in the eye, a while, and gets up again. */
async function crouch(g) {
  const m = g.actor("mariam");
  if (!m) return;
  m.look(661, 458);                                               // the nearest hen in the row
  await g.wait(250);
  await m.fidget("crouch");
  turnTo(g, "mariam");
}
const MARIAM_TREE = mariamTree({ crouch, aside: (g, on) => aside(g, on, "mariam") });
async function talkToMariam(g) {
  turnTo(g, "mariam");
  await g.talk(MARIAM_TREE);
  const m = g.actor("mariam");
  if (m) m.face("W");                                             // back to her hens
}
/** A carried thing shown to her: she turns to the boy, says what she makes of it, and goes back to her hens. */
const showMariam = (id) => async (g) => {
  turnTo(g, "mariam");
  await g.say(id);
  const m = g.actor("mariam");
  if (m) m.face("W");
};

/** The little case on the doorpost: what the boy makes of it, and the first time, Mariam's word for it. */
async function lookAtDoorpost(g) {
  await g.say("rome.tiber.doorpost.look");
  if (heard(g, "rome.mariam.doorpost.1") || !g.actor("mariam")) return;
  turnTo(g, "mariam");
  await g.say("rome.mariam.doorpost.1");
  g.actor("mariam").face("W");
}

// ---------- Felix, and his mother's lamp ----------

/** One of the scene's people as another state of himself, in the same place, facing the same way (as egypt-site.js does). */
function redraw(g, id, kind) {
  const cast = g.view.cast, old = g.actor(id);
  if (!old || old.kind === kind) return;
  cast.remove(id);
  try { cast.addFigure(id, kind, old.x, old.y, old.scale).face(old.yaw); }
  catch { cast.add(old); }
}
/** He sets his bale down on the pile beside him (`felix-free`), to have his hands free. */
async function setDown(g) {
  const f = g.actor("felix");
  if (!f) return;
  f.face("W");                                                    // (the pile of bales is on his left, at the landing's far end)
  await f.play(g.clock, "pick");
  redraw(g, "felix", "felix-free");
  await g.wait(250);
  turnTo(g, "felix");
}
/** The boy holds out the lamp, and Felix takes it: and with it, his word. */
async function handLamp(g) {
  const f = g.actor("felix"), me = g.lead;
  if (me) me.hold(true);
  await g.wait(500);
  if (f) await f.play(g.clock, "reach");
  g.take("lamp");
  g.flag("rome.felixWord", true);
  if (me) me.hold(false);
  await g.wait(400);
}
/** After the talk he takes up his bale again, and goes back to work. */
async function takeUpBale(g) {
  const f = g.actor("felix");
  if (!f || f.kind !== "felix-free") return;
  f.face("W");
  await g.wait(200);
  await f.play(g.clock, "pick");
  redraw(g, "felix", "felix");
  g.actor("felix").face("W");
}
const FELIX_TREE = felixTree({ setDown, lamp: handLamp, aside: (g, on) => aside(g, on, "felix") });
async function talkToFelix(g) {
  turnTo(g, "felix");
  await g.talk(FELIX_TREE);
  await takeUpBale(g);
  const f = g.actor("felix");
  if (f) f.face("W");
}
/** A carried thing shown to him: he turns to the boy, says his piece, and goes back to his bales. */
const showFelix = (id) => async (g) => {
  turnTo(g, "felix");
  await g.say(id);
  const f = g.actor("felix");
  if (f) f.face("W");
};

// ---------- the way out: back over the bridge ----------
/** Once the boy has seen the old man at his prayer, he has finished by the time the boy comes back: he is on his bench
    (rome.eleazarDown: set as the boy goes, before the scene changes, because the scene's people are placed when it is
    built). A game saved and loaded during the first visit still has him at his window. MAP-15: that is done by the
    scene's `leaving` (below), which runs however the boy leaves, over the bridge or by the map; the way only goes. */
function overTheBridge(g) {
  return g.goto("rome-forum", { spawn: "fromTiber" });
}

// ---------- the things: the painter's shapes, stands and facings (layout.json, "things") ----------
const HOUSE = [[824, 497], [558, 417], [558, 130], [824, 72]];
const house = { name: "house", poly: HOUSE, walkTo: [551, 433], face: "E", look: "rome.tiber.house.look" };
const windowThing = { name: "window", poly: [[637, 171], [726, 168], [726, 237], [638, 238]], walkTo: [528, 474], face: "E" };

export default {
  id: "rome-tiber",
  era: "rome",
  name: "Across the Tiber",
  // MAP-15: as the boy leaves, by the bridge or by the map, the old man has finished his prayer, once the boy has seen him at it
  leaving(g) { if (g.flag("rome.sawTiber")) g.flag("rome.eleazarDown", true); },
  music: "tiber",                                                 // the act's own quiet (js/content/sound.js)

  // DEPTH (fixed by the master brief, and the painter's camera): no minScale or maxScale is needed here. The farthest stand,
  // on the road at row 366, draws the boy 40 pixels tall.
  horizon: 250, full: 590,

  // The lane from the bridgehead to the road along the river, the little square with the well, and the landing. Not the
  // water, the barge, the hen yard or the house fronts.
  walk: { area: [[29, 598], [131, 497], [0, 497], [1, 497], [1, 462], [22, 452], [174, 452], [287, 341], [410, 341], [422, 377], [416, 379], [541, 418], [549, 418], [602, 434], [507, 446], [513, 448], [532, 456], [552, 464], [574, 473], [599, 482], [625, 492], [653, 504], [685, 516], [719, 530], [758, 545], [798, 561], [798, 598]] },
  blocked: [
    [[542, 415], [491, 399], [470, 401], [520, 417]],             // the bench (nobody can pass behind it: it stands 17 cm from the wall)
    [[0, 477], [16, 477], [58, 451], [5, 451]],                   // the pile of bales on the landing
  ],
  spawn: {
    default: [470, 528],
    fromBridge: [520, 562],                                       // off the bridge behind us (the painter's arrival mark: see `enter`)
  },
  exits: ["rome-forum"],
  // The way out across the edge of the picture: the bridge is behind us, so the bottom edge is the way back to the Forum,
  // wherever along it he is sent (from x 60 to 782 nothing to click covers its band).
  edges: {
    S: { to: "rome-forum", spawn: "fromTiber", name: "back over the stone bridge", walkTo: [520, 596], use: overTheBridge },
  },

  picture: art + "back.png",
  // The cut-outs, in the order to lay them (the painter's: S/work-rome-paint3/ready.md, section 8). Their bases are rows, or
  // the house front's foot line, so that the engine's order is the same whoever stands where.
  planes: [
    { id: "well", src: art + "well.png", base: 413, solid: [[356, 409], [353, 406], [343, 404], [330, 404], [317, 404], [307, 406], [302, 409], [304, 411], [313, 413], [327, 414], [341, 413], [352, 411]] },      // its kerb, and the bucket on it
    // The front of Eleazar's house round his upper window, the opening cut clear: a man standing in the room behind it
    // shows only through the window. Cut from the picture itself (laid over it, it changes nothing).
    { id: "window-wall", src: art + "window-wall.png", base: [[800, 490], [558, 417]] },
    { id: "washing", src: art + "washing.png", base: [[800, 490], [558, 417]] },     // the washing on its line (it sways), after the wall
    { id: "barge", src: art + "barge.png", base: 439 },          // it rides the water (`fx`, barge-bob); everyone on the landing is in front of it
    { id: "curb", src: art + "curb.png", base: 443 },            // the landing's far edge stones and its far bollard: in front of the barge's bow
    { id: "fence-corner", src: art + "fence-corner.png", base: 451, solid: [[517, 445], [524, 445], [533, 451], [517, 451]] },      // the yard's side fence and corner: the hens and Mariam behind it
    { id: "fence", src: art + "fence.png", base: 490, solid: [[599, 474], [627, 474], [627, 490], [599, 490]] },                     // the near run of the yard's fence
    { id: "landing-edge", src: art + "landing-edge.png", base: 501, solid: [[130, 501], [130, 498], [123, 496], [112, 496], [102, 498], [95, 501], [94, 505], [101, 507], [112, 507], [123, 505]] },      // the landing's near edge and its bollard
  ],

  // THINGS THAT MOVE BY NATURE (the painter's marks, layout.json "fx", as they are). Nothing that moves is painted still.
  fx: [
    // the sun on the river: glints that come, drift downstream (up and to the right) and go; the barge is a hole in it
    { id: "river-shimmer", type: "shimmer", poly: [[0, 271], [120, 265], [240, 258], [300, 255], [370, 262], [314, 311], [169, 446], [10, 446], [0, 448]], holes: [[[0, 403], [83, 271], [92, 271], [202, 307], [204, 309], [234, 350], [234, 354], [228, 368], [226, 370], [200, 390], [150, 428], [130, 443], [124, 447], [2, 453], [0, 453]]], count: 46, size: 7, flow: [3.5, -1.8], life: 1.6, color: "#fff4d8", opacity: 0.55 },
    // the water lapping along the barge, between it and the quay; and at the lowest step down from the landing (in the very
    // corner, under the inventory bar while the game waits for a click)
    { id: "barge-ripples", type: "ripples", at: [175, 406], radius: [3, 14], flat: 0.22, every: [1.2, 3], rings: 1, speed: 10, color: "#e8e4d8", trough: "#3e4a4a", opacity: 0.45 },
    { id: "barge-ripples-2", type: "ripples", at: [208, 381], radius: [2, 10], flat: 0.22, every: [1.6, 3.5], rings: 1, speed: 8, color: "#e8e4d8", trough: "#3e4a4a", opacity: 0.4, seed: 2 },
    { id: "steps-ripples", type: "ripples", at: [5, 590], radius: [2, 9], flat: 0.22, every: [1.4, 3.2], rings: 2, speed: 8, color: "#f0ead8", trough: "#4a4a40", opacity: 0.5, clip: [[[0, 505], [105, 505], [3, 600], [0, 600]]] },
    // the barge riding the water at its moorings (ENGINE-13R's `bob`: a pixel up and down; the water is painted whole under it)
    { id: "barge-bob", type: "bob", plane: "barge", amount: 1, period: 5 },
    // Mariam's five hens, each a flock of one on her own short perch, so that each keeps her colouring and her place in the
    // row: they stand, look up and shuffle, facing west over the river at the city, and never fly, turn or peck (they will not eat)
    ...[["brown", [[714, 485], [705, 482]]], ["speckled", [[697, 477], [689, 474]]], ["white", [[682, 468], [674, 465]]], ["brown", [[665, 460], [657, 457]]], ["speckled", [[648, 453], [641, 451]]]]
      .map(([set, perch], n) => ({ id: `hen-${n + 1}`, type: "birds", kind: "flock", perch, count: 1,
        frames: { foot: [24, 42], face: "W", sizeAt: 590, stand: [1, 2, 1, 3].map((k) => `hen-${set}-${k}.png`), look: [`hen-${set}-4.png`], walk: [`hen-${set}-5.png`, `hen-${set}-6.png`] },
        depth: true, shy: 0, fly: false, turn: false, walk: 4, moves: { stand: 3, look: 2, walk: 0.5, peck: 0, turn: 0 }, seed: n + 1 })),
    // the washing stirring on its line, hung from the top
    { id: "washing-sway", type: "sway", plane: "washing", anchor: "top", amount: 1, period: 3.6, wave: 40, lean: 0.3 },
    // a thin smoke from a cooking fire, behind the houses beyond the house of prayer
    { id: "cooking-smoke", type: "smoke", plane: "back", at: [492, 128], height: 70, width: [2, 14], lean: [-22, -70], rise: 10, rate: 2.5, gust: 0.3, color: "#f2ede6", opacity: 0.32 },
    // swallows over the river and the far bank: the temple steps' swallow frames, from that scene's folder. (The painter's
    // mark gives the folder beside `frames`; the engine reads it inside them, as egypt-crash.js gives its kites'.)
    { id: "birds-river", type: "birds", kind: "flyers", plane: "back", lanes: [[[-12, 132], [90, 112], [200, 128], [300, 96], [412, -12]], [[-12, 60], [80, 86], [170, 70], [260, 40], [330, -12]]], frames: { dir: "art/scenes/rome-steps/", flap: ["swallow-1.png", "swallow-2.png", "swallow-3.png", "swallow-2.png"], glide: "swallow-4.png", middle: [8, 5] }, scale: 1, every: [7, 16], group: [1, 2], speed: 110 },
    { id: "birds-far", type: "birds", kind: "flyers", plane: "back", lanes: [[[-12, 168], [100, 150], [210, 176], [330, 140], [360, -12]]], frames: { dir: "art/scenes/rome-steps/", flap: ["swallow-1.png", "swallow-2.png", "swallow-3.png", "swallow-2.png"], glide: "swallow-4.png", middle: [8, 5] }, scale: 0.55, every: [8, 18], group: [1, 3], speed: 70, seed: 3 },
  ],

  actors: [
    // Eleazar: at his upper window until he has come down (see "the old man at his window", above), then on his bench, under
    // the same id. At the window: his feet on the upper room's floor, a scale of his own, no ground of ours, his life his
    // own two movements. On the bench: found sitting, his scroll open; his life his own small movements (he unrolls his
    // scroll a little, reads with a finger, strokes his beard, looks up across the river), and he never leaves it.
    { id: "eleazar", kind: "eleazar-window", at: WINDOW, scale: WINDOW_SCALE, face: "W", solid: false, life: { fidget: [5, 11] }, when: (g) => !down(g) },
    { id: "eleazar", kind: "eleazar", at: BENCH, face: BENCH_FACE, life: { fidget: [6, 13] }, when: down },
    // Mariam in the hen yard, behind its fence, among her hens: now and then she goes to a corner of the yard and back
    // (her own ground: she walks in straight lines), scatters grain that nobody eats, counts her hens.
    { id: "mariam", kind: "mariam", at: MARIAM, face: "W",
      life: { every: [16, 30], spots: [[702, 486, "W"], [640, 458, "SW"]], stay: [3, 6] } },
    // Felix, with a bale on his shoulder, working between the landing and the barge's side (in front of the barge).
    { id: "felix", kind: "felix", at: FELIX, face: "W",
      life: { every: [10, 18], spots: [[75, 453, "NW"], [54, 475, "E"]], stay: [2, 4] } },
  ],

  // Back to front: a later area lies over an earlier one. The painter lists the things small before big ("where two shapes
  // overlap, the earlier one is meant"), so they are here in the painter's order turned round, and the people on top. The
  // shapes are the painter's (Show outlines them); the people's are their figures as the engine draws them at their marks.
  hotspots: [
    { id: "river", name: "river", verb: "Swim in", poly: [[0, 271], [120, 265], [240, 258], [300, 255], [370, 262], [314, 311], [169, 446], [10, 446], [0, 448]], walkTo: [237, 393], face: "W",
      look: "rome.tiber.river.look", use: "rome.tiber.river.use", useWith: { coin: "rome.tiber.river.coin", quarter: "rome.tiber.river.quarter" } },
    { id: "farbank", name: "far bank", poly: [[0, 148], [40, 146], [90, 154], [140, 168], [190, 186], [240, 212], [290, 234], [330, 244], [370, 250], [372, 256], [240, 260], [120, 266], [0, 272]], walkTo: [213, 418], face: "W",
      look: "rome.tiber.farbank.look" },
    // The road on along the river leads nowhere in this stage (the way out is the bridge, behind us): it is to look at.
    { id: "road", name: "road", poly: [[252, 375], [429, 375], [392, 280], [348, 280]], walkTo: [374, 366], face: "N", look: "rome.tiber.road.look" },
    { id: "gardens", name: "gardens", poly: [[300, 214], [442, 206], [442, 262], [300, 262]], walkTo: [374, 366], face: "N", look: "rome.tiber.gardens.look" },
    { id: "hens", name: "hens", verb: "Call", poly: [[549, 458], [799, 554], [799, 466], [650, 420], [650, 444]], walkTo: [562, 480], face: "E",      // the yard: its fence, its coop, its dish, and the hens in their row
      look: twice("rome.hens.look", "rome.hens.look2"), use: "rome.hens.use", useWith: { breakfast: "rome.hens.breakfast" } },
    { id: "prayerhouse", name: "house of prayer", verb: "Go in", poly: [[551, 418], [423, 378], [423, 175], [551, 152]], walkTo: [431, 392], face: "E",
      look: "rome.tiber.prayerhouse.look", use: "rome.tiber.prayerhouse.use" },
    // His house: while he prays, the boy would knock, and thinks better of it, and waits (the same for his door); after,
    // it is a house to look at.
    { id: "house", ...house, verb: "Knock at", when: (g) => !down(g), use: (g) => waitForHim(g, "rome.tiber.house.use") },
    { id: "house-2", ...house, when: down },
    { id: "doorway", ...house, name: "door", verb: "Knock at", poly: [[603, 430], [573, 421], [573, 319], [603, 322]], walkTo: [561, 429], when: (g) => !down(g), use: (g) => waitForHim(g, "rome.tiber.house.use") },
    { id: "barge", name: "barge", verb: "Climb onto", poly: [[0, 403], [83, 271], [92, 271], [202, 307], [204, 309], [234, 350], [234, 354], [228, 368], [226, 370], [200, 390], [150, 428], [130, 443], [124, 447], [2, 453], [0, 453]], walkTo: [140, 457], face: "W",
      look: "rome.tiber.barge.look", use: "rome.tiber.barge.use" },
    { id: "landing", name: "landing steps", verb: "Go down", poly: [[0, 497], [96, 497], [98, 457], [128, 457], [130, 505], [105, 505], [3, 600], [0, 600]], walkTo: [85, 483], face: "S",      // its near edge, the bollard and the steps down into the water
      look: "rome.tiber.landing.look", use: "rome.tiber.landing.use" },
    { id: "bales", name: "bales", verb: "Lift", poly: [[0, 407], [58, 397], [58, 451], [16, 477], [0, 477]], walkTo: [36, 487], face: "NW",
      look: "rome.tiber.bales.look", use: "rome.tiber.bales.use" },
    { id: "well", name: "well", poly: [[302, 368], [303, 367], [305, 366], [338, 356], [344, 356], [346, 357], [348, 359], [356, 369], [356, 378], [355, 413], [353, 414], [349, 415], [343, 416], [316, 416], [309, 415], [306, 414], [304, 413], [303, 412], [302, 375]], walkTo: [339, 419], face: "N",
      look: "rome.tiber.well.look", useWith: { coin: "rome.tiber.well.coin" } },
    // The bench: sitting is the main part of waiting (and while the old man prays, the boy waits there for him). The rig
    // cannot sit the Son down, so he waits standing at its near end.
    { id: "bench", name: "bench", verb: "Sit on", poly: [[470, 401], [486, 380], [534, 394], [542, 415], [520, 417]], walkTo: [520, 427], face: "N",
      look: "rome.tiber.bench.look", use: (g) => (down(g) ? g.say("rome.tiber.bench.use") : waitForHim(g, "rome.tiber.bench.use")) },
    { id: "figtree", name: "fig tree", verb: "Pick from", poly: [[651, 256], [654, 255], [665, 252], [691, 252], [799, 320], [799, 426], [799, 524], [799, 527], [796, 530], [794, 531], [784, 531], [782, 530], [780, 528], [779, 526], [651, 262]], walkTo: [674, 526], face: "E",
      look: "rome.tiber.figtree.look", use: "rome.tiber.figtree.use" },
    { id: "washing", name: "washing", poly: [[591, 192], [622, 190], [630, 190], [633, 192], [633, 205], [632, 228], [627, 231], [625, 232], [619, 233], [611, 233], [593, 223], [592, 222], [591, 209]], walkTo: [491, 450], face: "E",
      look: "rome.tiber.washing.look" },
    // His window: while he is at it, to wait under; once he has come down, to look at again.
    { id: "window", ...windowThing, verb: "Wait under", when: (g) => !down(g), look: "rome.tiber.window.look", use: (g) => waitForHim(g) },
    { id: "window-2", ...windowThing, when: down, look: "rome.tiber.window.look2" },
    { id: "doorpost", name: "little case", verb: "Poke", rect: [600, 351, 12, 20], walkTo: [576, 434], face: "E",       // fixed upright on the right-hand post of his door
      look: lookAtDoorpost, use: "rome.tiber.doorpost.use" },

    // The people. Felix on the landing, and Mariam in the yard (talked to from the lane outside the fence).
    {
      id: "felix", name: "boatman", verb: "Talk to", poly: [[61, 464], [68, 373], [70, 368], [75, 359], [78, 357], [85, 357], [98, 369], [102, 373], [104, 464], [102, 467], [98, 468], [90, 469], [75, 469], [67, 468], [63, 467]], walkTo: FELIX_TALK, face: "W",
      look: twice("rome.felix.look", "rome.felix.look2"), use: talkToFelix,
      useWith: { lamp: talkToFelix, gaultoga: showFelix("rome.felix.gaultoga"), coin: showFelix("rome.felix.coin"), breakfast: showFelix("rome.felix.breakfast") },
    },
    {
      id: "mariam", name: "girl", verb: "Talk to", poly: [[631, 475], [632, 437], [636, 411], [638, 404], [640, 403], [643, 401], [648, 401], [651, 403], [654, 406], [662, 475], [659, 478], [652, 479], [641, 479], [634, 478]], walkTo: MARIAM_TALK, face: "E",
      look: twice("rome.mariam.look", "rome.mariam.look2"), use: talkToMariam,
      useWith: { gaultoga: showMariam("rome.mariam.gaultoga"), coin: showMariam("rome.mariam.coin"), quarter: showMariam("rome.mariam.quarter"),
        gum: showMariam("rome.mariam.gum"), breakfast: showMariam("rome.mariam.breakfast"), lamp: showMariam("rome.mariam.lamp") },
    },
    // The old man: at his window, his area is the window's opening (Show outlines his own figure inside it); the boy waits
    // for him. Down, on his bench, his figure there.
    { id: "atwindow", name: "old man", verb: "Wait for", actor: "eleazar", poly: OPENING, walkTo: WAIT, face: "NE", when: (g) => !down(g),
      look: twice("rome.eleazar.look.window", "rome.eleazar.look.window2"), use: (g) => waitForHim(g) },
    {
      id: "eleazar", name: "old man", verb: "Talk to", poly: [[484, 378], [485, 373], [494, 352], [498, 349], [503, 349], [506, 352], [512, 363], [515, 370], [516, 373], [517, 378], [514, 417], [487, 417], [484, 379]], walkTo: WAIT, face: "W", when: down,
      look: twice("rome.eleazar.look", "rome.eleazar.look2"), use: talkToEleazar,
      useWith: { coin: "rome.eleazar.coin", quarter: "rome.eleazar.quarter", lamp: "rome.eleazar.lamp", breakfast: "rome.eleazar.breakfast" },
    },
  ],

  // Runs as the scene is built, and after a save is loaded. (Where the old man is, the actors' entries say: the fact
  // rome.eleazarDown. Felix always has his bale on his shoulder when the scene is built: he puts it down only to talk.)
  setup(g) {
    // On his bench the old man's face is just where the words of anyone talking near him go (the boy beside the bench,
    // at the window's stand, walking off down the lane): the sprite flag `clear` lifts their words over his head.
    if (down(g) && g.actor("eleazar")) g.actor("eleazar").flag("clear", true);
  },

  // Runs when the lead arrives. It must be safe to run twice, so it checks its own fact.
  // The first time, he comes off the bridge, takes a step, and stops: the old man at his window, praying; the girl among
  // her hens, all of them in a row (the design's 5.7). Later, he walks a step in from the bridge.
  async enter(g, from) {
    const me = g.lead;
    if (g.flag("rome.sawTiber")) {
      if (from === "rome-forum") await g.walkTo(STEP_IN[0], STEP_IN[1]);
      return;
    }
    await g.wait(300);
    await g.walkTo(STEP_IN[0], STEP_IN[1]);
    if (!down(g)) {                                               // (he is at his window: always so the first time, in a game played)
      if (me) me.face("N");
      await g.wait(500);
      await g.say("rome.tiber.arrive.1");
      if (me) me.look(WINDOW[0], WINDOW[1] - 60);                 // up at the window
      await g.wait(400);
      await g.say("rome.tiber.arrive.2");
      if (me) me.face("S");                                       // and to us
      await g.say("rome.tiber.arrive.3");
      if (me) me.face("N");
    }
    g.flag("rome.sawTiber", true);
  },
};

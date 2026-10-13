// Act Two: the Capitol, the precinct of Jupiter Best and Greatest (ROME-13S2: new in round thirteen; briefs/ROME-13.md,
// SCENES-13R.md and SCENES-13R2.md; the design is briefs/out/rome2-design.md, 2.2, 4.3 and 5.5).
// Rome, the morning of the Ides of March, 44 B.C. The Son plays.
//
// The top of the Capitol: the walled sacred precinct before the greatest temple in Rome, far off across the paving, with
// its altar, the dictator's chariot and his bronze man on the world before its steps; the row of the old kings' statues in
// the middle, old Brutus with his sword among them; Romulus's hut, the geese's pen and, over the parapet, the whole city to
// the west: the river and its island, Pompey's great theater on the plain, the hill across the Tiber.
//
//   chain B   (NEW 3, Juno's Geese) The keeper's boy, Titus, took the soothsayer's breakfast at first light, went after the
//             Ides ewe as he does every Ides, and is sitting on top of the middle statue base among the kings with the
//             breakfast in his lap: the sacred geese stand round its foot, and whenever he puts a foot down every neck comes
//             out and they hiss. Calling them, shooing them, and everything the boy carries, tried on them: they hiss. The
//             goose-keeper, Anser, will not move them, but ask him about his geese and he tells, at length, how they saved
//             the city when the Gauls climbed the hill: "They cannot abide anything strange. They shout at it, and then they
//             run." The boy is the strangest thing in Rome: he stomps, his sneakers flash red, and the geese shriek, flap and
//             run for their pen. Titus hops down, hands over the breakfast, and runs home down the hill.
//
// The two talks are dialogue trees (titusTree and anserTree in js/content/talk/rome.js), and the scripts a branch needs are
// handed to them as hooks: Titus's `feet`, the goose-keeper's `shake` and `stomp` (the solution: the same script as a click
// on the geese once he has told his tale). The lines are in js/content/lines/rome.en.js (the writer's ids.md, part 1, "The
// Capitol", says which is said when).
//
// The geese are the engine's (`fx`, a flock: ENGINE-13R's herd and pose), painted frame by frame by PAINT-13R2. Nothing of
// a herd is saved: the scene's `fx` is a function of the game, and gives the flock its place from the fact rome.geeseGone
// whenever the scene is built (round the foot of the base, or in the pen).
//
// Every place below is the painter's own measurement of the finished picture (art/scenes/rome-capitol/layout.json, and
// S/work-rome-paint2/ready.md), or was set by eye against the picture with the people standing in it; where the two differ
// the comment says why.
//
// Try it: index.html?scene=rome-capitol&lead=son&flags=rome.arrived,rome.knowsBC
// Later states: add rome.sawCapitol, rome.knowsBoy, rome.metTitus, rome.metAnser, rome.knowsGeese ... rome.geeseGone,rome.hasBreakfast

import { titusTree, anserTree } from "../talk/rome.js";

const art = "art/scenes/rome-capitol/";

// ---------- where things are (layout.json: marks) ----------
const FROM_STEPS = [540, 560];          // marks.fromSteps: in at the gate, at the bottom (behind us), facing N
const TO_STEPS = [540, 595];            // marks.toSteps: the bottom way's walkTo
const STEP_IN = [526, 528];             // a step up into the precinct from the gate, out of the bottom band (set by eye)
const AT_BASE = [384, 506];             // marks.atbase: before the boy's base, by its right corner, in front of the geese
// The goose-keeper behind his pen, facing E (his geese, the base). The painter's marks.anser is [146, 458]: there his feet
// are 22 pixels behind the pen's far fence, which would hide his shins, but the far fence is painted in the backdrop, so
// he was drawn over it, standing on it. Here he is the painter's x, 21 pixels farther back, at the foot of the parapet:
// his feet just behind the top of the far fence, where nothing of him should be hidden by it.
const ANSER = [146, 437];
const VIEW = [202, 439];                // marks.view: at the parapet, facing W; between the pen's back and the kings
const TITUS_RUN = [468, 594];           // marks.titus_run: where Titus runs out at the bottom
const TITUS_SEAT = [336, 447];          // marks.titus_seat.at: the ground under his hips, at the foot of the base's front face
                                        // (its height, 120 cm, is CAPITOL_BASE_SEAT in js/art/people.js: PEOPLE-13R's)
/** marks.geese: round the foot of the base, in front of it: where the geese stand guard. */
const GEESE = [[284, 450], [406, 450], [401, 485], [273, 485]];
/** Inside the pen: where they run to and stay. The painter's marks.pen is [[101, 509], [219, 509], [232, 492], [123, 492]];
    its right-hand side is drawn in by ten pixels here, off the pen's right-hand fence, so that no goose stands on a rail
    (ENGINE-13R: keep a herd's place a little in from the fence). ROME-13T: and both ends brought in from the ends of the
    near fence (pen.png: x 72 to 238 along its foot), by the most a goose reaches out in front of or behind its feet (its
    neck stretched out low, `look`: 62 of the frame's pixels, 47 at the pen's row), so that no goose's head or tail shows
    past an end of the fence, as if it stood half outside. Was [[101, 509], [209, 509], [222, 492], [123, 492]]. */
const PEN = [[119, 509], [191, 509], [194, 492], [123, 492]];
const PEN_GATE = [249, 496];            // marks.pen_gate: the gap the gate leaves, in the pen's right-hand side (two geese abreast)
// Where Titus comes to give the boy the breakfast, once he has hopped down off the base: a step to the boy's left, on the
// ground the geese have left (set by eye).
const HAND_OVER = [344, 503];
// Where the boy talks to the goose-keeper: beside him, on the strip of paving between the pen and the parapet (never in
// front of his face); the same row, for the same reason as his.
const BY_ANSER = [196, 438];

/** The geese (layout.json `frames.geese`): one picture a frame, every frame 116 x 104 with the feet at 54, 98, facing E, the
    right size at row 590. With `set`, 4 is "goose-4.png". 1-2 stand, 3-4 look (the neck out low, hissing), 5-8 walk,
    9-12 run (wings half open), 13 turn, 14-15 peck, 16-17 flap. */
const GOOSE = { set: "goose", foot: [54, 98], face: "E", sizeAt: 590, stand: [1, 2], look: [3, 4], walk: [5, 6, 7, 8], run: [9, 10, 11, 12], turn: [13], peck: [14, 15], flap: [16, 17] };

/** Has this line been spoken yet? (The engine counts every line it says.) */
const heard = (g, id) => !!g.store.data.seenLines[id];
/** How many times a line has been spoken. */
const times = (g, id) => g.store.data.seenLines[id] || 0;
/** A thing worth looking at twice: the first line the first time, the second after that. */
const twice = (first, second) => (g) => g.say(heard(g, first) ? second : first);
/** Someone who can stand turns to the boy. */
const turnTo = (g, who) => { const a = g.actor(who), me = g.lead; if (a && me) a.look(me.x, me.y); };
const gone = (g) => !!g.flag("rome.geeseGone");
/** The flock, for a script: guarded as the steps' pigeons are. (With no moving things, ?nofx, it is off the stage, and its
    herd and its pose are over at once: the puzzle still plays, and ends the same.) */
const geeseOf = (g) => (g.effects && g.effects.get("geese")) || null;

/** One of the scene's people as another state of himself, in the same place, facing the same way (as egypt-site.js does it). */
function redraw(g, id, kind) {
  const cast = g.view.cast, old = g.actor(id);
  if (!old || old.kind === kind) return;
  cast.remove(id);
  try { cast.addFigure(id, kind, old.x, old.y, old.scale).face(old.yaw); }
  catch { cast.add(old); }
}

// ---------- ROME-13S2: the sneakers, copied from js/content/scenes/rome-street.js (a scene file takes nothing from another) ----------
/** His sneakers light up when he stomps: a blink of red on the paving under his feet. */
async function stomp(g) {
  const glow = g.q("#stomp"), me = g.lead;
  g.sfx("plug");
  if (!glow || !me) return g.wait(300);
  glow.setAttribute("cx", me.x);
  glow.setAttribute("cy", me.y);
  for (let n = 0; n < (g.calm ? 1 : 2); n++) {                    // one soft glow for players who asked for less motion
    await g.tween(g.calm ? 300 : 110, (k) => glow.setAttribute("opacity", k));
    await g.tween(g.calm ? 500 : 190, (k) => glow.setAttribute("opacity", 1 - k));
  }
}

// ---------- the geese, on guard round the foot of the base ----------

/** Every goose stretches its neck out low and hisses, for a moment, while the line is said. */
async function hiss(g, ...ids) {
  const geese = geeseOf(g), hissing = geese ? geese.pose("look", 1.2) : null;
  g.sfx("goosehiss");
  await g.say(...ids);
  if (hissing) await hissing;
}

/** A click on the geese: calling them and shooing them, in turn, each with a hiss; once the goose-keeper has told how they
    saved the city, the stomp. */
async function atTheGeese(g) {
  if (g.flag("rome.knowsGeese")) return stompTheGeese(g);
  return hiss(g, times(g, "rome.geese.call") > times(g, "rome.geese.shoo") ? "rome.geese.shoo" : "rome.geese.call");
}

/** Everything he carries, tried on them: a word, and a hiss. */
const tryOnGeese = (...items) => Object.fromEntries(items.map((item) => [item, (g) => hiss(g, `rome.geese.${item}`)]));

// ---------- the solution: the stomp ----------
/**
 * The goose-keeper's tale is the instructions: "They cannot abide anything strange. They shout at it, and then they run."
 * The boy, before the base, says so, and stomps: his sneakers flash red twice; the geese shriek, flap and run for their
 * pen, the nearest to him first, through the gap the gate leaves (the engine's herd), and they are in. Titus hops down,
 * comes over, and hands the breakfast to the boy; then he runs home, down the hill and out at the bottom. The goose-keeper
 * has the last word. (The anser tree's hook `stomp`, and a click on the geese after the tale.)
 */
async function stompTheGeese(g) {
  const me = g.lead, anser = g.actor("anser");
  await g.walkTo(AT_BASE[0], AT_BASE[1]);
  if (me) me.face("N");
  await g.say("rome.geese.stomp");
  await stomp(g);
  const geese = geeseOf(g);
  if (anser) anser.look(PEN_GATE[0], PEN_GATE[1]);                // he turns to see his geese come
  g.sfx("geese");
  if (geese && me) await geese.herd(PEN, { from: [me.x, me.y], via: PEN_GATE });
  g.flag("rome.geeseGone", true);
  if (me) me.look(PEN_GATE[0], PEN_GATE[1]);                      // where they went
  await g.wait(300);
  g.sfx("honk");                                                  // one last word from the pen
  await g.wait(400);

  // Titus hops down off the base (PEOPLE-13R's hop: onto his feet in front of it, the bundle clutched to him)
  let titus = g.actor("titus");
  if (me && titus) me.look(titus.x, titus.y);
  if (titus) await titus.sit(false);
  await g.say("rome.titus.down");
  // and comes over to the boy with the breakfast, holding it out by its knot
  if (titus) {
    await g.walkTo(HAND_OVER[0], HAND_OVER[1], "titus");
    if (me) { titus.look(me.x, me.y); me.look(titus.x, titus.y); }
    titus.hold(true);
  }
  await g.say("rome.titus.give");
  // (he came up the hill before the keeper said a word, or stomped before he ever spoke to Titus: whose boy, whose
  // breakfast, is said now; and so before the breakfast changes hands, in the order of the beats)
  if (!g.flag("rome.knowsBoy")) g.flag("rome.knowsBoy", true);
  if (!g.flag("rome.metTitus")) g.flag("rome.metTitus", true);
  await g.reach();
  if (titus) titus.hold(false);
  g.give("breakfast");
  g.flag("rome.hasBreakfast", true);
  redraw(g, "titus", "titus-free");                               // nothing in his hands now, and ready to run home
  titus = g.actor("titus");
  await g.say("rome.titus.give.son");
  await g.say("rome.titus.run");
  // home: down the hill, at a run, and out at the bottom (the gate is behind us)
  if (titus) {
    await g.walkTo(TITUS_RUN[0], TITUS_RUN[1], "titus");
    await g.moveTo(TITUS_RUN[0] + 6, 660, "titus");
    g.view.cast.remove("titus");
  }
  if (me && anser) { me.look(anser.x, anser.y); anser.look(me.x, me.y); }
  await g.say("rome.anser.last");
  if (anser) anser.face("E");
}

// ---------- Titus, on the base ----------
/** The hook `feet`: his feet dangle, every goose stretches its neck and hisses, and he draws his feet up to his chin. */
async function feet(g) {
  const titus = g.actor("titus"), geese = geeseOf(g), hissing = geese ? geese.pose("look", 1.2) : null;
  g.sfx("goosehiss");
  await g.wait(220);
  if (titus) await titus.fidget("feet");
  if (hissing) await hissing;
}
const TITUS_TREE = titusTree({ feet });
async function talkToTitus(g) {
  const titus = g.actor("titus"), me = g.lead;
  if (me && titus) me.look(titus.x, titus.y - 60);                // up at him, on his base
  await g.talk(TITUS_TREE);
}

// ---------- the goose-keeper, behind his pen ----------
/** The hook `shake`: he shakes his basket of grain. */
async function shake(g) {
  const anser = g.actor("anser");
  if (anser) await anser.fidget("shake");
}
const ANSER_TREE = anserTree({ shake, stomp: stompTheGeese });
async function talkToAnser(g) {
  turnTo(g, "anser");
  await g.talk(ANSER_TREE);
  const anser = g.actor("anser");
  if (anser) anser.face("E");                                     // back to his geese
}

// ---------- the view: the theater is where the Senate meets today, though nobody here says so ----------
async function lookAtTheater(g) {
  await g.say(heard(g, "rome.capitol.theater.look") ? "rome.capitol.theater.look2" : "rome.capitol.theater.look");
  g.flag("rome.sawTheater", true);
}

export default {
  id: "rome-capitol",
  era: "rome",
  name: "The Capitol",

  // DEPTH (layout.json). minScale is the painter's: the temple stands far off, its lowest step at rows 320 to 326, where a
  // man is 23 to 25 pixels tall in true perspective; with the engine's own floor (0.26) he would be half again too big
  // beside the painted steps.
  horizon: 275, full: 590, minScale: 0.15,

  // The paving from the gate at the bottom to the temple's lowest step on the right and to the parapet on the left; never
  // behind the kings (the far line runs along the front of the row).
  walk: { area: [[0, 597], [797, 597], [797, 322], [478, 326], [483, 332], [477, 450], [214, 450], [228, 431], [0, 431]] },
  // The five kings' bases (painted into the backdrop: nobody walks behind them).
  blocked: [
    [[214, 448], [256, 448], [264, 438], [224, 438]],
    [[256, 448], [299, 448], [304, 438], [264, 438]],             // old Brutus's
    [[298, 448], [374, 448], [376, 433], [307, 433]],             // the middle one, broad and low: Titus's
    [[373, 448], [415, 448], [414, 438], [374, 438]],             // the new statue's
    [[415, 448], [457, 448], [454, 438], [414, 438]],
  ],
  spawn: { default: [500, 520], fromSteps: FROM_STEPS },
  facing: "N",                                                    // in at the gate, looking up the precinct
  exits: ["rome-steps"],
  // The way out across the edge of the picture: the precinct's gate is behind us, at the bottom, where the road from the
  // Forum comes in (the bottom band from x 400 to 640 is open paving).
  edges: {
    S: { to: "rome-steps", spawn: "fromCapitol", name: "down the hill to the steps", walkTo: TO_STEPS },
  },

  picture: art + "back.png",
  // CUT-OUTS, in the painter's order (layout.json `planes`), each with the ground it takes up. The backdrop is complete
  // under each. Not cut-outs: the kings and their bases (nobody walks behind them) and the temple (beyond the walk).
  planes: [
    { id: "altar", src: art + "altar.png", base: [[539, 359], [691, 359]], solid: [[539, 359], [691, 359], [667, 352], [528, 352]] },        // the great altar on its step
    { id: "chariot", src: art + "chariot.png", base: [[693, 375], [778, 375]], solid: [[693, 375], [778, 375], [725, 362], [652, 362]] },  // the dictator's chariot, facing Jupiter's doors
    { id: "world", src: art + "world.png", base: [[483, 381], [521, 381]], solid: [[483, 381], [521, 381], [515, 376], [479, 376]] },      // his bronze man on the world, on its tall base
    // the parapet over the drop: a base line, not the front plane (the boy stands at it to look at the view); the city's
    // smoke rises behind it
    { id: "parapet", src: art + "parapet.png", base: [[-136, 429], [228, 429]], solid: [[-676, 429], [228, 429], [235, 423], [-632, 423]] },
    { id: "hut", src: art + "hut.png", base: 465, solid: [[116, 447], [119, 439], [102, 433], [69, 431], [27, 433], [-14, 439], [-46, 447], [-58, 456], [-44, 464], [-6, 467], [44, 464], [89, 456]] },   // Romulus's hut
    // the pen's near fence and its gate side, the gate swung right back: the geese in the pen stand behind it (its far
    // fence, the trough and the straw are in the backdrop)
    { id: "pen", src: art + "pen.png", base: [[73, 515], [233, 515]], solid: [[69, 516], [235, 516], [260, 480], [118, 480]] },
    // the four bronze tablets on their posts, running away from us at the front right: people pass behind them (the base
    // runs along the posts' left side)
    { id: "tablets", src: art + "tablets.png", base: [[739, 590], [628, 487]], solid: [[[747, 590], [793, 590], [772, 573], [729, 573]], [[704, 551], [744, 551], [728, 538], [690, 538]], [[670, 520], [706, 520], [693, 510], [659, 510]], [[643, 496], [675, 496], [665, 487], [634, 487]]] },
  ],

  // THINGS THAT MOVE BY NATURE (the painter's marks, layout.json "fx", as they are), and the geese. A function of the
  // game (ENGINE-13R): the flock's place, and how it passes the time, follow rome.geeseGone whenever the scene is built.
  fx: (g) => [
    // the last of the morning's smoke from the altar (the Ides ewe went up at first light: this is all that is left of
    // it), thin and pale, leaning left with the air, and a few coals still red in the ash: both at the altar's base, so
    // that anyone behind the altar is behind its smoke
    { id: "altar-smoke", type: "smoke", at: [606, 320], base: [[539, 359], [691, 359]], height: 150, width: [3, 18], lean: [-38, -150], rise: 14, rate: 2.5, gust: 0.3, color: "#f2ece2", opacity: 0.4 },
    { id: "altar-embers", type: "embers", at: [606, 320], size: [34.4, 1.6], count: 6, sparks: 0.08, base: [[539, 359], [691, 359]], glowOpacity: 0.12 },
    // Juno's sacred geese: round the foot of the boy's base, on guard (standing, looking about, never shy, never flying),
    // until the stomp; after it, in their pen, mostly eating, as if nothing had happened
    { id: "geese", type: "birds", kind: "flock", area: gone(g) ? PEN : GEESE, count: 6, frames: GOOSE, shy: 0, fly: false, walk: 30,
      moves: gone(g) ? { stand: 1.5, look: 0.5, peck: 5, walk: 1.5, turn: 1 } : { stand: 4, look: 3, peck: 0.5, walk: 1, turn: 1 } },
    // two kites wheeling high over the precinct, in the open sky left of the temple
    { id: "kites", type: "birds", kind: "flyers", circle: { at: [250, 96], r: [120, 34] }, count: 2, speed: 14, size: 11, plane: "back" },
    // threads of smoke from the city below, behind the parapet
    { id: "city-smoke-1", type: "smoke", at: [150, 364], plane: "back", height: 34, width: [1, 6], lean: [-12, -34], rise: 5, rate: 1.5, gust: 0.2, color: "#ece6dc", opacity: 0.26 },
    { id: "city-smoke-2", type: "smoke", at: [138, 374], plane: "back", height: 26, width: [1, 5], lean: [-10, -26], rise: 4, rate: 1.3, gust: 0.2, color: "#ece6dc", opacity: 0.22, seed: 2 },
    { id: "city-smoke-3", type: "smoke", at: [182, 306], plane: "back", height: 18, width: [1, 4], lean: [-8, -18], rise: 3, rate: 1.2, gust: 0.2, color: "#eee8de", opacity: 0.2, seed: 3 },
    // a faint light on the river, round the island (kept clear), and on its far reach where it shows between the theater
    // and the kings
    { id: "river-light", type: "shimmer", plane: "back", count: 6, size: 3, flow: [2, 0], life: 2.2, color: "#f4fbff", opacity: 0.32,
      poly: [[236, 299], [227, 302], [218, 305], [208, 307], [196, 311], [182, 315], [166, 319], [145, 323], [120, 326], [92, 332], [60, 334], [26, 336], [26, 349], [60, 348], [92, 347], [120, 348], [145, 346], [166, 343], [182, 337], [196, 331], [208, 323], [218, 315], [227, 310], [236, 305], [236, 305]],
      holes: [[[104, 338], [126, 332], [152, 327], [176, 324], [196, 320], [210, 309], [219, 310], [212, 324], [206, 330], [186, 335], [160, 340], [155, 350], [140, 350], [132, 344], [108, 344]]] },
    { id: "river-light-far", type: "shimmer", plane: "back", poly: [[140, 298], [170, 299], [201, 299], [201, 304], [170, 303], [140, 302]], count: 2, size: 2, flow: [1.5, 0], life: 2.4, color: "#f4fbff", opacity: 0.26 },
  ],

  // The one piece of light up here, as in the street: his sneakers. A soft red glow on the paving under his feet, hidden
  // until he stomps. (ROME-13S2: copied from rome-street.js.)
  live() {
    return `<defs><radialGradient id="stomp-glow"><stop offset="0" stop-color="#ff6a52" stop-opacity="0.95"/><stop offset="0.5" stop-color="#ff4a3d" stop-opacity="0.6"/><stop offset="1" stop-color="#ff4a3d" stop-opacity="0"/></radialGradient></defs>
      <ellipse id="stomp" cx="0" cy="0" rx="40" ry="12" fill="url(#stomp-glow)" opacity="0" shape-rendering="geometricPrecision"/>`;
  },

  actors: [
    // Titus, found sitting on top of the middle base (its height is CAPITOL_BASE_SEAT: PEOPLE-13R's), facing us, the
    // breakfast in his lap, until he has handed it over. He blocks no ground: he is up on the base, and the base is blocked.
    // His life is his own small movements only (he waves at the boy, peeks into the cloth, pretends to be a statue).
    { id: "titus", kind: "titus", at: TITUS_SEAT, face: "S", solid: false, when: (g) => !g.flag("rome.hasBreakfast"), life: { still: true } },
    // The goose-keeper behind his pen, facing his geese: now and then a few steps along the back of it and back, and he
    // shakes his basket, leans on his stick, counts them, sighs. While they guard the base he goes to look at them over
    // there; once they are in the pen, to look in at them over its fence. (He does not walk out among them round the base:
    // the way there from behind his pen crosses the far fence, which is in the backdrop and would be drawn behind him. One
    // person, two entries with opposite `when`s: the first whose `when` holds is the one he lives by.)
    { id: "anser", kind: "anser", at: ANSER, face: "E", when: (g) => !gone(g),
      life: { every: [20, 40], spots: [[204, 438, "E"], [178, 438, "E"]], stay: [3, 6] } },
    { id: "anser", kind: "anser", at: ANSER, face: "E", when: gone,
      life: { every: [20, 40], spots: [[204, 438, "S"], [178, 438, "S"]], stay: [3, 6] } },
  ],

  // Back to front: a later area lies over an earlier one (the painter's order, with the geese and the people last).
  // SHAPES: the painter's (layout.json `things`), each hugging its thing; the people's are their figures as the engine
  // draws them at their marks.
  hotspots: [
    { id: "temple", name: "temple of Jupiter", verb: "Climb", walkTo: [620, 392], face: "N", look: "rome.capitol.temple.look", use: "rome.capitol.temple.use",
      poly: [[784, 81], [802, 290], [802, 322], [728, 323], [451, 327], [450, 327], [446, 326], [352, 301], [349, 300], [347, 299], [347, 269], [352, 167], [426, 65], [429, 61], [431, 59], [611, 0], [618, -2], [619, -2], [780, 76]] },
    { id: "name", name: "letters on the front", walkTo: [620, 392], face: "N", look: "rome.capitol.name.look", poly: [[475, 107], [736, 117], [736, 102], [475, 91]] },
    { id: "roof", name: "gold roof", walkTo: [620, 392], face: "N", look: "rome.capitol.roof.look", poly: [[428, 83], [586, 2], [638, 2], [781, 98], [781, 89], [428, 74]] },
    { id: "doors", name: "temple doors", walkTo: [620, 392], face: "N", look: "rome.capitol.doors.look", poly: [[463, 265], [606, 265], [606, 187], [463, 184]] },
    {
      id: "altar", name: "great altar", verb: "Touch", plane: "altar", walkTo: [612, 376], face: "N", look: "rome.capitol.altar.look", use: "rome.capitol.altar.use",
      useWith: { incense: "rome.capitol.altar.incense" },
      poly: [[526, 348], [531, 319], [533, 315], [535, 312], [662, 312], [682, 316], [684, 318], [687, 322], [693, 354], [693, 360], [536, 360], [526, 354]],
    },
    { id: "chariot", name: "bronze chariot", verb: "Climb into", plane: "chariot", walkTo: [726, 392], face: "N", look: "rome.capitol.chariot.look", use: "rome.capitol.chariot.use",
      poly: [[650, 324], [655, 282], [657, 279], [667, 255], [720, 255], [743, 256], [780, 331], [780, 377], [692, 378], [668, 370], [651, 363]] },
    { id: "world", name: "bronze man on a ball", plane: "world", walkTo: [500, 398], face: "N", look: "rome.capitol.world.look",
      poly: [[523, 260], [521, 383], [482, 383], [481, 382], [479, 379], [475, 271], [475, 267], [476, 261], [490, 201], [492, 192], [493, 190], [497, 183], [511, 175], [512, 175], [513, 176]] },
    // The row of kings: the hull of the three old kings, which also covers Brutus and the new statue: those two are listed
    // after it, so that they win, and Titus's own area after them all.
    { id: "kings", name: "statues of kings", walkTo: [440, 476], face: "N", look: twice("rome.capitol.kings.look", "rome.capitol.kings.look2"),
      poly: [[456, 224], [460, 361], [460, 370], [458, 450], [213, 450], [212, 364], [226, 267], [234, 250], [252, 235], [308, 209], [309, 209], [455, 220]] },
    { id: "brutus", name: "statue with a sword", walkTo: [272, 468], face: "N", look: "rome.capitol.brutus.look", poly: [[255, 450], [255, 236], [309, 209], [310, 209], [315, 380], [314, 450]] },
    { id: "dictator", name: "shiny new statue", walkTo: [404, 478], face: "N", look: "rome.capitol.dictator.look", poly: [[372, 450], [371, 369], [381, 268], [383, 266], [389, 255], [392, 252], [416, 240], [417, 240], [416, 450]] },
    { id: "tablets", name: "bronze tablets", verb: "Read", plane: "tablets", walkTo: [664, 566], face: "E", look: "rome.capitol.tablets.look", use: "rome.capitol.tablets.use",
      poly: [[794, 592], [747, 592], [744, 590], [635, 491], [632, 488], [625, 434], [625, 411], [670, 410], [735, 442], [782, 466], [784, 468], [791, 481], [802, 500], [802, 515]] },
    { id: "hut", name: "little round hut", verb: "Knock at", plane: "hut", walkTo: [52, 497], face: "N", look: "rome.capitol.hut.look", use: "rome.capitol.hut.use",
      poly: [[-2, 469], [-2, 346], [29, 319], [33, 319], [131, 393], [133, 395], [133, 399], [111, 450], [107, 452], [95, 456], [38, 470]] },
    // The pen, until the geese are in it (then the area over it is the geese's: below)
    { id: "pen", name: "goose pen", verb: "Open", plane: "pen", walkTo: [272, 505], face: "W", when: (g) => !gone(g), look: "rome.capitol.pen.look", use: "rome.capitol.pen.use",
      poly: [[236, 517], [70, 517], [69, 516], [69, 465], [70, 464], [83, 456], [93, 450], [114, 437], [116, 436], [272, 429], [273, 429], [274, 430], [275, 434], [275, 468], [274, 474], [237, 516]] },
    // The geese on guard round the foot of the base: one area, one verb, so calling them and shooing them come in turn;
    // everything he carries, tried on them; and once the goose-keeper has told his tale, the stomp.
    {
      id: "geese", name: "sacred geese", verb: "Shoo", walkTo: AT_BASE, face: "N", when: (g) => !gone(g),
      look: twice("rome.geese.look", "rome.geese.look2"), use: atTheGeese,
      useWith: tryOnGeese("gum", "quarter", "coin", "phone", "toga", "gaultoga", "lamp", "tunic"),
      poly: [[267, 410], [412, 410], [412, 489], [267, 489]],
    },
    // ... and after the stomp, the geese in their pen: the pen's own shape
    { id: "geese", name: "sacred geese", walkTo: [272, 505], face: "W", when: gone, look: "rome.geese.penned", use: "rome.geese.penned.use",
      poly: [[236, 517], [70, 517], [69, 516], [69, 465], [70, 464], [83, 456], [93, 450], [114, 437], [116, 436], [272, 429], [273, 429], [274, 430], [275, 434], [275, 468], [274, 474], [237, 516]] },
    // Over the parapet, the city to the west: all three are looked at from the parapet (marks.view)
    { id: "view", name: "river and island", walkTo: VIEW, face: "W", look: "rome.capitol.view.look", poly: [[112, 336], [126, 326], [196, 318], [236, 300], [236, 312], [214, 330], [180, 346], [124, 352], [112, 346]] },
    { id: "theater", name: "stone half-circle", walkTo: VIEW, face: "W", look: lookAtTheater, poly: [[0, 284], [64, 270], [130, 284], [196, 302], [196, 322], [0, 318]] },
    { id: "janiculum", name: "hill across the river", walkTo: VIEW, face: "W", look: "rome.capitol.janiculum.look", poly: [[0, 246], [120, 238], [236, 250], [236, 296], [130, 292], [0, 294]] },
    // The people. Each area is the figure as the engine draws it at its mark, a few pixels outside its edge.
    {
      // Titus up on the base: talked to from before it (marks.atbase), looking up at him
      id: "titus", name: "keeper's boy", verb: "Talk to", walkTo: AT_BASE, face: "NW", when: (g) => !g.flag("rome.hasBreakfast"),
      look: twice("rome.titus.look", "rome.titus.look2"), use: talkToTitus,
      useWith: { toga: "rome.titus.toga", gaultoga: "rome.titus.toga", coin: "rome.titus.coin", quarter: "rome.titus.quarter", gum: "rome.titus.gum" },
      poly: [[342, 348], [341, 360], [346, 363], [349, 372], [345, 381], [346, 413], [325, 413], [326, 381], [324, 369], [325, 363], [330, 360], [329, 348]],
    },
    {
      // The goose-keeper: talked to from beside him, on the paving behind the pen
      id: "anser", name: "goose-keeper", verb: "Talk to", walkTo: BY_ANSER, face: "W",
      look: twice("rome.anser.look", "rome.anser.look2"), use: talkToAnser,
      useWith: { toga: "rome.anser.toga", gaultoga: "rome.anser.toga", coin: "rome.anser.coin", quarter: "rome.anser.quarter", gum: "rome.anser.gum", breakfast: "rome.anser.breakfast" },
      poly: [[162, 345], [162, 381], [165, 387], [162, 396], [162, 443], [133, 443], [133, 438], [128, 435], [140, 429], [139, 417], [135, 414], [137, 372], [141, 366], [139, 360], [142, 354], [155, 351], [155, 345]],     // (with his stick)
    },
  ],

  // Runs as the scene is built, and after a save is loaded. Titus sits high on his base, and the boy talks to him from
  // below: his face is just where the boy's words, and the goose-keeper's, would go, so the engine lifts them over his
  // head (the sprite flag `clear`, as for Grandma Jolene behind her counter). And the goose-keeper, a big man behind his
  // pen, farther back than the boy at the pen, the hut or the geese: the same.
  setup(g) {
    for (const id of ["titus", "anser"]) { const a = g.actor(id); if (a && a.flag) a.flag("clear", true); }
  },

  // Runs when the lead arrives. It must be safe to run twice, so it checks its own fact.
  async enter(g, from) {
    if (from === "rome-steps") await g.walkTo(STEP_IN[0], STEP_IN[1]);      // in at the gate, and a step up into the precinct
    if (g.flag("rome.sawCapitol")) return;
    const me = g.lead, titus = g.actor("titus");
    await g.wait(300);
    if (me) me.face("N");                                         // the temple, at the far end of the precinct
    await g.say("rome.capitol.arrive.1");
    if (me) me.face("W");                                         // and the city, over the parapet
    await g.say("rome.capitol.arrive.2");
    if (titus && !g.flag("rome.hasBreakfast")) {                  // (a game saved before the bigger Rome may have its breakfast already: then nobody is up there)
      if (me) me.look(titus.x, titus.y - 60);                     // and the kings, and who is sitting on top of one of them
      g.sfx("honk");
      await g.say("rome.capitol.arrive.3");
    }
    g.flag("rome.sawCapitol", true);
  },
};

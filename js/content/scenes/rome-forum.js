// Act Two: the Forum, from its east end (ROME-13S1: new in round thirteen; briefs/ROME-13.md, SCENES-13R.md and
// SCENES-13R1.md; the place is the design's 2.1, briefs/out/rome2-design.md). The morning of the Ides of March, 44 B.C.
// The Son plays.
//
// The open heart of Rome, seen from the rise of the Sacred Way and looking west along it: at the far end, small, the
// temple of Saturn, where the act began (the way back to the steps); over everything the Capitol, Jupiter's gilt roof on
// fire with the sun. Down the left, the corner of Castor's temple, Juturna's spring before it, and the mouth of the Tuscan
// street (the way down to the river and across it); then Caesar's basilica, still in scaffolding. Down the right, the
// basilica of Paullus, and before it the site of the new senate house, a hoarding round a hole, with a treadwheel crane.
// In the square, the stone ring of the Puteal, a moneychanger's table waiting for him, and statues on tall columns.
//
// Two people of the act's three new puzzles are here:
//   chain A   the Gaul (NEW 2, Nobody Will Show Him: the tree `gaulTree`). A senator from the Province, the first day of
//             his first meeting, in front of the hoarding where the senate house ought to be, in a toga far too short for
//             him: the Roman senator's, from the laundry. Nobody will show a new senator the way to the House (a notice
//             says so: it is a joke, and he is it). Told where the Senate meets today (the senator said so on the steps,
//             rome.knowsSenate), he has his answer; given his own toga (the boy has it from the senator), he goes behind
//             the hoarding, comes out a senator, gives the boy the senator's, and goes off to the Senate (rome.swapped).
//   chain C   Phyllis (NEW 4, Interest Is Extra Wishes, her side: `phyllisTree`), on her stool among her baskets at the
//             foot of Castor's temple. The coin the boy borrowed from the fountain was her wish (Walnut says so in the
//             street, rome.knowsWish): she threw it in for her son Felix, who is going to Corinth, with a little clay lamp
//             she cannot take him, for she cannot leave her baskets on the busiest morning of the spring. The boy takes the
//             lamp across the river (rome.hasLamp); when Felix has given his word (rome.felixWord), she lets him keep the
//             coin (rome.wishGranted), which the toss in the treasury waits for.
// Everything else here is to look at, with a word from the boy for each thing (js/content/lines/rome.en.js, the Forum's
// part; S/work-rome-writer/ids.md part 1, "The Forum"). Every place below is the painter's own measurement of the
// finished picture (art/scenes/rome-forum/layout.json and S/work-rome-paint1/ready.md), or was set against the picture
// with the people standing in it; where the two differ the comment says why.
//
// Try it: index.html?scene=rome-forum&lead=son&flags=rome.arrived,rome.knowsBC
// Later states: add rome.wrongToga, rome.knowsSenate (and game.give("gaultoga")) for the Gaul; rome.hasCoin, rome.knowsWish
// (and game.give("coin")) for Phyllis; rome.hasLamp, rome.felixWord for her leave.

import { gaulTree, phyllisTree } from "../talk/rome.js";
import { scaleAt } from "../../engine/walk.js";            // the size of a row, for the people's own walks in the scripts below

const art = "art/scenes/rome-forum/";
const STEPS = "art/scenes/rome-steps/";                     // the pigeons and the swallows are the steps' own painted frames

/** Has this line been spoken yet? (The engine counts every line it says.) */
const heard = (g, id) => !!g.store.data.seenLines[id];
/** A thing worth looking at twice: the first line the first time, the second after that. */
const twice = (first, second) => (g) => g.say(heard(g, first) ? second : first);
/** Someone who can stand turns to the boy. */
const turnTo = (g, who) => { const a = g.actor(who), me = g.lead; if (a && me) a.look(me.x, me.y); };
/** A hand kept held out (the people's rig), asked for through a guard, so that a figure without it simply stands. */
const hold = (a, on) => a && a.hold && a.hold(on);
/** One of the scene's people as another state of himself, in the same place, facing the same way (as egypt-site.js does it). */
function redraw(g, id, kind) {
  const cast = g.view.cast, old = g.actor(id);
  if (!old || old.kind === kind) return;
  cast.remove(id);
  try { cast.addFigure(id, kind, old.x, old.y, old.scale).face(old.yaw); }
  catch { cast.add(old); }
}
/** One of the scene's people walks somewhere on the square, round whatever is in the way (the ground as they have it:
    their own place free, and the boy standing in it), at the size of each row. */
async function stroll(g, id, to) {
  const f = g.actor(id), scene = g.scene;
  if (!f || !f.walkPath) return;
  await f.walkPath(g.clock, g.groundFor(id).path([f.x, f.y], to), (y) => scaleAt(scene, y));
}

// ---------- where things are (layout.json: marks) ----------
const TO_STEPS = [329, 281];          // the top way's walkTo: the foot of Saturn's steps, at the far end
const FROM_STEPS = [341, 284];        // arriving from the steps (small: 18 pixels, under the temple)
const TO_TIBER = [136, 306];          // in the Tuscan street's mouth, behind Castor's corner, wholly hidden by its cut-out
const FROM_TIBER = [214, 318];        // a step out of the mouth
// Where he has walked to on arriving, before he looks about him (`enter`). From the steps: a good way down the middle of
// the square, from where his temple is "way down at the end" and the crane and the gold roof are both in view (the
// arrival's lines are written for here, not for the foot of Saturn's steps). From the river: out of the street's mouth
// onto the square, clear of the first statue's plinth.
const DOWN_THE_SQUARE = [392, 432];
const OUT_OF_THE_STREET = [252, 352];

// The Gaul (marks.gaul and the rest): in front of the hoarding's open gateway, facing the site and the crane. He is 1.08
// tall: 80.8 pixels here, so that the short toga reads. The gateway, and just inside it by the near gatepost the place
// behind the near boards where a man standing is wholly hidden (he changes togas there).
const GAUL = [650, 401];
const GAUL_SPOTS = [[577, 368, "NE"], [685, 418, "E"], [528, 452, "W"]];      // along the hoarding's far part, its near part, and toward the middle
const GATE = [641, 379];
const BEHIND = [690, 389];
// Where the boy stands to talk to him: beside him on his left, a step nearer us, clear of his face and of the gateway (the
// painter's stand for the crane, which the Gaul stands under).
const AT_GAUL = [610, 420];
// Where he goes, once he has his own toga and his way: up the square toward its far right end, where the plain lies
// beyond the basilica of Paullus, between the site and the colonnade, until the square leaves the picture.
const GAUL_GOES = [576, 300];

// Phyllis (marks.phyllis): the ground under her hips on her low stool (drawn with her), among her baskets at the foot of
// Castor's temple, facing the square; and where she stands to hang a garland on her pole (marks.phyllis_stand).
const PHYLLIS = [181, 481];
const PHYLLIS_STAND = [214, 478];
// Where the boy stands to talk to her: on her right, a step nearer us and clear of her pole's foot, so that she can get up
// and go to her pole past him (the painter's stand for the garlands, [232, 492], is a few pixels too near the way she goes).
const AT_PHYLLIS = [246, 494];

// ---------- the pigeons ----------
// The flocks on the square are the engine's (`fx`, below): they potter, peck, and go up when somebody comes near. The
// painter marks one area for where they potter; as a thing to click it would lie over the whole middle of the square, and
// a click meant for the floor there would chase pigeons instead of walking. So, as on the steps (rome-steps.js), each
// of the seven near birds is a thing to click, its area going with it (a few times a second, round the bird as it is
// drawn now: the first area round the first bird, and so on), Show outlining the bird itself; an area with no bird for it
// (they have flown off) is put away until one comes back. The three far up the square are left to the floor. With no
// moving things at all (?nofx), there are no birds, and no areas.
const FLOCKS = ["pigeons", "pigeons-dark"];
const BIRDS = 7;                                            // five, and two dark ones
/** The steps' pigeon frames (rome-steps.js, PIGEON), as the painter marks them here: no shadow (the steps' painted shadow
    falls the wrong way for this sun), the right size at row 590 and smaller farther off, as people are. */
const PIGEON = (set) => ({ dir: STEPS, set, foot: [23, 40], face: "E", sizeAt: 590, stand: [1, 3], look: [2], peck: [4, 5], walk: [6, 7, 8, 9], turn: [10],
  takeoff: [11, 12], fly: [13, 14, 15], glide: [17], land: [18], shadow: null });
const SWALLOW = { dir: STEPS, flap: ["swallow-1.png", "swallow-2.png", "swallow-3.png", "swallow-2.png"], glide: "swallow-4.png", middle: [8, 5] };
/** Where they potter: the square in the sun, off the walkers' line up the middle (layout.json: fx, and the thing `pigeons`). */
const SQUARE = [[300, 440], [520, 420], [690, 468], [712, 540], [420, 544], [250, 536]];

/** "Chase": he says he is not chasing them, and does a little, and up they all go (as on the steps). */
async function chase(g, at = null) {
  const me = g.lead;
  if (me && at) {                                                 // one quick step at them
    const dx = at[0] - me.x, dy = at[1] - me.y, d = Math.hypot(dx, dy) || 1, step = Math.min(24, d * 0.5);
    me.look(at[0], at[1]);
    await g.walkTo(me.x + (dx / d) * step, me.y + (dy / d) * step);
  }
  for (const id of FLOCKS) { const flock = g.effects && g.effects.get(id); if (flock && flock.scare) flock.scare(at || (me ? [me.x, me.y] : null), 260); }
  await g.say("rome.forum.pigeons.use");
}
const pigeons = { name: "pigeons", verb: "Chase", look: "rome.forum.pigeons.look", use: (g) => chase(g) };
/** Where a pigeon is painted in its frames (46 by 50, its feet at 23, 40): 15 to the left or right of them, 17 above them
    on the ground (in flight its wings go 28 above), 2 below (rome-steps.js). */
const BIRD_BOX = { half: 16, up: 18, flying: 29, down: 3 };
/** The pigeons' areas go with them. Called a few times a second, on the game's clock (as on the steps). */
function movePigeonAreas(g) {
  const view = g.view, cast = view && view.cast;
  if (!cast) return;
  const birds = [];
  for (const flock of FLOCKS) for (let n = 0; ; n++) {
    const b = cast.get(`fx:${flock}:${n}`);
    if (!b) break;
    const pic = !b.hidden && b.picture ? b.picture(cast.palette, cast.calm) : null;
    if (!pic || !pic.canvas) continue;
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

// ---------- the crane's great wheel, and the dust where it sets a block down ----------
// The wheel is painted frames (crane-0 to crane-5, a sixth of a spoke further round in each: `planes`), and the block
// hanging from the crane is painted and does not rise. So the wheel is still most of the time (frame 0 is the wheel as
// the backdrop has it), turns now and then for a few seconds, two whole turns of its spokes, and stops; and just after,
// a little pale dust comes up where a block is set down on the new wall, for six or seven seconds (the painter's note).
// On the game clock, so it stops with the menu; none of it is saved. With less motion, the wheel stays on frame 0.
const TURN_MS = 4000;                                       // 12 frames at 3 a second: two whole turns, back to frame 0
const crane = { stop: null };
function craneLife(g) {
  if (crane.stop) { crane.stop(); crane.stop = null; }
  const scene = g.scene, clock = g.clock, wheel = g.plane("crane-wheel");
  if (!wheel) return;
  wheel.flag("still", true);
  let phase = "rest", turns = 0, until = clock.now + 11000;
  crane.stop = clock.every((dt, now) => {
    if (g.scene !== scene) { crane.stop(); crane.stop = null; return; }
    if (now < until) return;
    const dust = g.effects && g.effects.get("crane-dust");
    if (phase === "rest") { wheel.now = 0; wheel.flag("still", false); phase = "turn"; until = now + TURN_MS; }
    else if (phase === "turn") { wheel.flag("still", true); if (dust) dust.show(true); phase = "dust"; until = now + 6500; }
    else { if (dust) dust.show(false); phase = "rest"; turns++; until = now + (30 + ((turns * 13) % 21)) * 1000; }      // the next in 30 to 50 seconds
  });
}

// ---------- chain A: the Gaul ----------
/** The hook `point`: he turns to the site and points at the hole where the House was (over the hoarding, where the new wall
    is rising out of it), and lowers his arm, and turns back to the boy to say so. */
async function point(g) {
  const gaul = g.actor("gaul");
  if (!gaul) return;
  gaul.face("NE");
  await g.wait(200);
  if (gaul.fidget) await gaul.fidget("point");
  turnTo(g, "gaul");
}
/** The hook `bow`: deep and formal, from the hips, his hand to his heart, to the boy who does not know either. */
async function bow(g) {
  const gaul = g.actor("gaul");
  if (!gaul) return;
  turnTo(g, "gaul");
  if (gaul.fidget) await gaul.fidget("bow");
}
/** The hook `swap`: the boy holds out the enormous toga, and the Gaul takes it; he goes into the hoarding's gateway and
    behind the near boards, where nobody can see him; a while; and he comes out again in his own toga, falling properly, and
    hands the boy the senator's, folded. (He walks in straight lines: the gateway is off the floor the boy walks on.) */
async function swap(g) {
  const me = g.lead;
  await g.reach();                                                // the Gaul's toga, held out, and taken
  g.take("gaultoga");
  if (!g.actor("gaul")) { g.give("toga"); g.flag("rome.swapped", true); return; }
  await g.moveTo(GATE[0], GATE[1], "gaul");                       // into the gateway
  await g.moveTo(BEHIND[0], BEHIND[1], "gaul");                   // and behind the near boards: not a hair of him shows
  await g.wait(900);
  redraw(g, "gaul", "gaul-own");                                  // (nobody sees it: he is wholly behind the hoarding)
  await g.wait(1100);
  await g.moveTo(GATE[0], GATE[1], "gaul");
  await g.moveTo(GAUL[0], GAUL[1], "gaul");                       // out again, a senator to his ankles
  const gaul = g.actor("gaul");
  if (gaul && me) gaul.look(me.x, me.y);
  await g.wait(300);
  hold(gaul, true);                                               // the senator's toga, folded, held out
  await g.reach();                                                // and taken
  hold(gaul, false);
  g.give("toga");
  g.flag("rome.swapped", true);
}
/** The hook `leave`: he goes off up the square toward its far right end, where the plain lies beyond the basilica, and
    is gone where the square leaves the picture. (rome.swapped keeps him off the Forum from then on: see `actors`.) */
async function leave(g) {
  const gaul = g.actor("gaul");
  if (!gaul) return;
  await stroll(g, "gaul", GAUL_GOES);
  await g.tween(600, (k) => gaul.fade(1 - k));
  g.view.cast.remove("gaul");
}
const GAUL_TREE = gaulTree({ point, bow, swap, leave });
/** Talked to (or his own toga held out to him): his talk. Then he turns back to the hoarding, if he is still here. */
async function talkToGaul(g) {
  turnTo(g, "gaul");
  await g.talk(GAUL_TREE);
  const gaul = g.actor("gaul");
  if (gaul && !g.flag("rome.swapped")) gaul.face("E");
}

// ---------- chain C: Phyllis ----------
/** The hook `stand`: she gets up off her stool, goes to her pole, hangs a garland on it, comes back and sits again. */
async function stand(g) {
  const ph = g.actor("phyllis");
  if (!ph || !ph.sit) return;
  await ph.sit(false);
  await stroll(g, "phyllis", PHYLLIS_STAND);
  ph.face("E");                                                   // to her pole
  if (ph.fidget) await ph.fidget("hang");
  await stroll(g, "phyllis", PHYLLIS);
  ph.face("SE");
  await ph.sit(true);
}
/** The hook `lamp`: she unwraps the little lamp in her lap and holds it out in both hands; the boy takes it, like an egg.
    The lamp is gone from her lap: a half-made garland in her hands instead (`phyllis-free`; her stool is drawn with her,
    so it is where it was). */
async function lamp(g) {
  const ph = g.actor("phyllis");
  if (ph && ph.fidget) { ph.fidget("offer", { hold: true }); await g.wait(900); }
  await g.reach();                                                // and taken
  g.give("lamp");
  g.flag("rome.hasLamp", true);
  if (ph && ph.fidget) ph.fidget(null);
  redraw(g, "phyllis", "phyllis-free");
}
/** The hook `grant`: her leave. The coin is his to keep. */
async function grant(g) {
  g.flag("rome.wishGranted", true);
  await g.wait(400);
}
const PHYLLIS_TREE = phyllisTree({ stand, lamp, grant });
const talkToPhyllis = (g) => g.talk(PHYLLIS_TREE);

// ---------- the ways out ----------
/** The far temple and the street's mouth are ways too, each the same as its edge: up the square to the foot of Saturn's
    steps, and back to them; into the Tuscan street's mouth, and down to the river. */
async function toSteps(g) {
  await g.walkTo(TO_STEPS[0], TO_STEPS[1]);
  await g.goto("rome-steps", { spawn: "fromForum" });
}
async function toTiber(g) {
  await g.walkTo(TO_TIBER[0], TO_TIBER[1]);                       // into the mouth, behind Castor's corner
  await g.goto("rome-tiber", { spawn: "fromBridge" });
}

export default {
  id: "rome-forum",
  era: "rome",
  name: "The Forum",

  // DEPTH (layout.json). minScale is the painter's: 0.15 is the true scale at the far end, the foot of Saturn's steps, so
  // that his temple is small and far off there (the square is told shorter than it is, the Capitol at its true distance).
  horizon: 235, full: 590, minScale: 0.15,

  // The square, from the bottom edge to the foot of Saturn's steps; into the mouth of the Tuscan street at the left; along
  // the front of the hoarding (60 cm short of it) at the right, and up between the site and the colonnade of Paullus.
  walk: { area: [[0, 597], [797, 597], [770, 446], [527, 342], [528, 341], [590, 294], [560, 285], [547, 284], [520, 285], [491, 285], [462, 285], [433, 285], [403, 285], [375, 284], [370, 284], [367, 280], [315, 281], [283, 282], [250, 295], [124, 297], [122, 320], [184, 329], [173, 392], [152, 477], [0, 488]] },
  // Ground that things painted into the backdrop stand on: the spring's basin's front corner, Phyllis's baskets, and the
  // foot of her pole of garlands. (The cut-outs' own footprints are their `solid`, below.)
  blocked: [
    [[108, 500], [148, 500], [156, 492], [118, 492]],
    [[154, 471], [193, 471], [200, 464], [162, 464]],
    [[236, 471], [255, 471], [258, 466], [238, 466]],
  ],
  spawn: {
    default: [420, 470],
    fromSteps: FROM_STEPS,                                        // at the far end, at the foot of Saturn's steps (see `enter`)
    fromTiber: FROM_TIBER,                                        // a step out of the Tuscan street's mouth
    fromHouse: [600, 556],                                        // (for later: the bottom edge, the Sacred Way to the chief priest's house)
  },
  exits: ["rome-steps", "rome-tiber"],
  // The ways out across the edges of the picture (the contract's table). The top band is open sky right of the temple of
  // Jupiter (74% of it covered by nothing), and a click there walks him up the square to the foot of Saturn's steps; the
  // left band is floor below row 508, in front of the basin, and a click there walks him into the Tuscan street's mouth,
  // out of sight behind Castor's corner. There is no way out at the bottom in this stage: its band is plain floor.
  edges: {
    N: { to: "rome-steps", spawn: "fromForum", name: "back to the steps of Saturn's temple", walkTo: TO_STEPS },
    W: { to: "rome-tiber", spawn: "fromBridge", name: "down the Tuscan street, over the river", walkTo: TO_TIBER },
  },

  picture: art + "back.png",
  // CUT-OUTS, in the painter's order (layout.json `planes`), each with its base and the ground it takes up. The hoarding is
  // two cut-outs, cut at the middle of its gateway (the near part, from the near gatepost, hides the Gaul at BEHIND), and
  // the crane's wheel sorts as if it stood a row above the hoarding's far end (so that it is behind everyone in front of
  // the boards): the painter laid them so for the engine's old depth order (ready.md, section 8), and they are kept so.
  planes: [
    { id: "statue-3", src: art + "statue-3.png", base: 294.3, solid: [[350, 294], [370, 294], [371, 293], [351, 293]] },
    { id: "statue-2", src: art + "statue-2.png", base: 308.3, solid: [[520, 308], [545, 308], [540, 306], [516, 306]] },
    { id: "statue-1", src: art + "statue-1.png", base: 330.9, solid: [[245, 331], [278, 331], [283, 327], [251, 327]] },
    // the crane's great wheel: still, mostly (see craneLife)
    { id: "crane-wheel", frames: [0, 1, 2, 3, 4, 5].map((n) => art + `crane-${n}.png`), fps: 3, at: [645, 354], foot: [34, 152], base: 340.1 },
    { id: "castor", src: art + "castor.png", base: [[133.7, 473.4], [156.4, 392.5]] },          // its column strip too: whoever is in the street's mouth is behind it
    { id: "puteal", src: art + "puteal.png", base: [[338, 394.4], [415, 394.4]], solid: [[417, 387], [409, 382], [390, 380], [366, 380], [346, 382], [336, 387], [342, 391], [362, 394], [388, 394], [409, 391]] },
    { id: "table", src: art + "table.png", base: [[412, 399.8], [489, 399.8]], solid: [[411, 400], [490, 400], [483, 386], [410, 386]] },
    { id: "awning", src: art + "awning.png", base: [[411, 399.8], [491, 399.8]] },
    { id: "hoarding", src: art + "hoarding.png", base: [[543.4, 342.1], [620.8, 373.1]] },
    { id: "hoarding-near", src: art + "hoarding-near.png", base: [[654.7, 386.7], [850.4, 465.1]] },
    { id: "basin", src: art + "basin.png", base: 507.5, solid: [[-175, 507], [112, 507], [142, 479], [-116, 479]] },
    { id: "front-base", src: art + "front-base.png", base: 511.8, solid: [[737, 512], [862, 512], [812, 482], [700, 482]] },   // the empty statue base at the front right: people pass behind it
  ],

  // THINGS THAT MOVE BY NATURE (layout.json `fx`, as the painter marks them). Nothing that moves is painted.
  fx: [
    // the thread of smoke from the Ides offering before the temple of Jupiter, far up on the Capitol (the same smoke as the steps' far view)
    { id: "hill-smoke", type: "smoke", plane: "back", at: [179, 112], height: 46, width: [1, 6], lean: [14, -46], rise: 6, rate: 2, gust: 0.2, color: "#f4ecde", opacity: 0.35 },
    // Juturna's spring: the water coming in from the spout at the back of the basin, the rings where it falls, the light on
    // the still water (half a row in front of the basin's base: over its water, and behind anyone standing in front of it)
    { id: "spring-stream", type: "stream", path: [[43.0, 437.1], [35.2, 441.1], [29.4, 455.0]], width: [2.0, 3.0], speed: 40, splash: 3, opacity: 0.55, base: 508.0 },
    { id: "spring-ripples", type: "ripples", at: [29, 455], radius: [1, 12], flat: 0.3, every: [0.9, 1.6], rings: 2, speed: 10, opacity: 0.5, base: 508.0, clip: [[0, 469], [105, 469], [129, 450], [0, 450]] },
    { id: "spring-shimmer", type: "shimmer", poly: [[0, 469], [105, 469], [129, 450], [0, 450]], clip: [[0, 469], [105, 469], [129, 450], [0, 450]], count: 5, size: 5, flow: [3, 0], life: 2.0, opacity: 0.4, base: 508.0 },
    // pigeons on the square, in the sun, off the walkers' line up the middle; and a few more far up the square, small
    { id: "pigeons", type: "birds", kind: "flock", area: SQUARE, count: 5, frames: PIGEON("pigeon") },
    { id: "pigeons-dark", type: "birds", kind: "flock", area: SQUARE, count: 2, frames: PIGEON("pigeon-dark"), seed: 2 },
    { id: "pigeons-far", type: "birds", kind: "flock", area: [[300, 330], [500, 320], [560, 360], [300, 372]], count: 3, frames: PIGEON("pigeon"), seed: 3 },
    // swallows, back for the spring, only in the open sky right of the temple of Jupiter
    { id: "swallows", type: "birds", kind: "flyers", plane: "back", lanes: [[[380, -12], [420, 30], [470, 60], [560, 64], [660, 40], [812, 30]], [[812, 90], [700, 72], [600, 86], [500, 70], [420, 30], [400, -12]]],
      frames: SWALLOW, scale: 0.7, every: [7, 16], group: [1, 3], speed: 90 },
    // the moneychanger's little awning stirring over his table
    { id: "awning-sway", type: "sway", plane: "awning", anchor: "top", amount: 1.0, period: 3.6, lean: 0.2 },
    // a little pale dust where the crane sets a block down on the new wall: only now and then, just after the wheel has
    // turned (craneLife shows it, and takes it away again); behind the hoarding and the wheel, and behind anyone on the square
    { id: "crane-dust", type: "smoke", at: [612, 276], base: 338.1, height: 26, width: [6, 26], lean: [10, -20], rise: 8, rate: 3, gust: 0.4, color: "#e8d4a8", opacity: 0.3, when: () => false },
  ],

  actors: [
    // The Gaul, at the hoarding, until the togas are swapped: then he has gone to the Senate, for good. He walks along the
    // hoarding and back, and out toward the middle of the square, asking passers-by the way; he tugs the short toga down,
    // looks up at the crane, folds his arms, asks the air and shrugs (his own small movements: js/art/people.js).
    { id: "gaul", kind: "gaul", at: GAUL, face: "E", when: (g) => !g.flag("rome.swapped"),
      life: { every: [16, 30], spots: GAUL_SPOTS, stay: [3, 7] } },
    // Phyllis, found sitting on her stool, the lamp in her lap; and the same woman, the lamp given, a half-made garland in her
    // hands instead (a script swaps her in place as she gives it: `lamp`). Now and then she gets up to hang a garland on her
    // pole and sits again; sitting, she weaves, sniffs a violet, counts her coins, looks across the square.
    { id: "phyllis", kind: "phyllis", at: PHYLLIS, face: "SE", when: (g) => !g.flag("rome.hasLamp"),
      life: { every: [24, 46], spots: [[PHYLLIS_STAND[0], PHYLLIS_STAND[1], "E"]], stay: [3, 5], stand: true } },
    { id: "phyllis", kind: "phyllis-free", at: PHYLLIS, face: "SE", when: (g) => !!g.flag("rome.hasLamp"),
      life: { every: [24, 46], spots: [[PHYLLIS_STAND[0], PHYLLIS_STAND[1], "E"]], stay: [3, 5], stand: true } },
  ],

  // Back to front: a later area lies over an earlier one. Each shape is the painter's (layout.json `things`), which hugs
  // its thing; each stand place and facing is the painter's but where the comment says otherwise.
  hotspots: [
    // ---- the Capitol, over everything, and the far end of the square (looked up at from the middle of the square)
    { id: "jupiter", name: "temple of Jupiter", poly: [[174, 107], [174, 114], [179, 114], [180, 118], [190, 116], [191, 124], [196, 124], [219, 113], [221, 117], [225, 117], [227, 113], [232, 114], [234, 110], [239, 111], [241, 108], [379, 119], [379, 105], [374, 103], [374, 75], [379, 73], [381, 61], [346, 54], [217, 39], [215, 37], [217, 29], [213, 29], [210, 32], [209, 27], [205, 27], [205, 41], [188, 69], [191, 80], [194, 81], [194, 107], [184, 113], [183, 107]],
      walkTo: [400, 440], face: "N", look: twice("rome.forum.jupiter.look", "rome.forum.jupiter.look2") },
    { id: "moneta", name: "temple of Juno", poly: [[624, 65], [603, 57], [601, 53], [596, 53], [593, 57], [573, 62], [556, 71], [553, 78], [553, 113], [561, 112], [576, 105], [623, 106], [622, 74], [624, 73]],
      walkTo: [400, 440], face: "N", look: twice("rome.forum.moneta.look", "rome.forum.moneta.look2") },
    { id: "records", name: "record office", poly: [[296, 124], [296, 131], [298, 132], [298, 245], [561, 245], [561, 133], [564, 131], [562, 123]],
      walkTo: [400, 440], face: "N", look: "rome.forum.records.look" },
    { id: "paullus", name: "basilica of Paullus", poly: [[799, 100], [729, 120], [721, 120], [538, 184], [539, 277], [725, 332], [725, 130], [798, 106]],
      walkTo: [505, 352], face: "E", look: twice("rome.forum.paullus.look", "rome.forum.paullus.look2") },
    // The far temple is also the way back. Its look is said from where he stands, not from the painter's stand (which is
    // the way back itself, at the foot of its steps): "That's MY temple, way down there." A click walks him there, and on.
    { id: "saturn", name: "temple of Saturn", verb: "Walk to", poly: [[438, 168], [375, 145], [364, 143], [290, 165], [271, 176], [268, 180], [293, 173], [294, 182], [270, 192], [270, 245], [266, 246], [266, 270], [289, 278], [301, 278], [308, 281], [448, 279], [447, 274], [440, 264], [440, 249], [436, 248], [435, 187], [436, 171]],
      look: twice("rome.forum.saturn.look", "rome.forum.saturn.look2"), use: toSteps },
    { id: "rostra", name: "speakers' platform", verb: "Climb", poly: [[373, 233], [373, 235], [381, 236], [381, 243], [373, 245], [374, 284], [485, 286], [507, 284], [545, 284], [546, 244], [538, 245], [531, 243], [532, 235], [545, 235], [545, 233], [495, 233], [494, 230], [491, 229], [491, 217], [494, 211], [491, 212], [489, 208], [486, 209], [485, 229], [482, 230], [481, 233], [469, 233], [468, 230], [465, 229], [465, 216], [468, 211], [465, 211], [463, 208], [461, 208], [459, 212], [459, 229], [455, 230], [454, 233], [432, 233], [430, 223], [433, 214], [431, 214], [428, 218], [427, 208], [423, 209], [424, 217], [420, 220], [420, 229], [418, 233]],
      walkTo: [452, 290], face: "N", look: "rome.forum.rostra.look", use: "rome.forum.rostra.use" },
    // ---- down the left: Caesar's basilica and its scaffolding, Castor's temple, the street's mouth
    { id: "julia", name: "Caesar's basilica", poly: [[262, 175], [244, 167], [233, 167], [226, 165], [225, 167], [103, 167], [103, 295], [244, 295], [262, 288]],
      walkTo: [232, 312], face: "N", look: "rome.forum.julia.look" },
    { id: "scaffold", name: "scaffolding", verb: "Climb", poly: [[270, 156], [267, 157], [267, 176], [261, 175], [261, 288], [266, 286], [267, 288], [271, 288], [285, 282], [285, 165]],
      walkTo: [290, 292], face: "W", look: "rome.forum.scaffold.look", use: "rome.forum.scaffold.use" },
    { id: "castor", name: "temple of Castor", verb: "Climb", plane: "castor", poly: [[0, 0], [0, 483], [134, 474], [174, 332], [174, 214], [159, 202], [159, 0]],
      walkTo: [196, 420], face: "N", look: twice("rome.forum.castor.look", "rome.forum.castor.look2"), use: "rome.forum.castor.use" },
    // The street's mouth is the way to the river: a look from its edge, and a click walks him into it, and on. The street
    // itself runs off to the left behind Castor's corner, out of sight; the painter's shape for it ([174, 111] down to
    // [174, 329]) lies over the near end of Caesar's basilica, its arches in Castor's shadow, and the hill above its roof,
    // where a player sees a building and a hill. So the thing to click is the shadowed opening of the street on the ground,
    // at the basilica's foot (the painter's own lower edge), and the arches above it are the basilica's.
    { id: "tuscan", name: "Tuscan street", verb: "Walk to", poly: [[174, 296], [243, 296], [238, 298], [180, 321], [174, 329]],
      walkTo: [214, 318], face: "W", look: "rome.forum.tuscan.look", use: toTiber },
    // ---- down the right: the site of the new senate house, and its crane
    { id: "site", name: "building site", verb: "Go into", poly: [[563, 221], [563, 224], [575, 225], [575, 270], [563, 272], [563, 276], [574, 276], [575, 282], [568, 283], [560, 280], [556, 282], [553, 279], [537, 277], [537, 340], [615, 371], [618, 376], [625, 375], [647, 384], [651, 390], [662, 390], [799, 445], [799, 274], [760, 274], [759, 259], [723, 258], [723, 272], [721, 273], [720, 259], [711, 258], [711, 262], [747, 341], [748, 346], [745, 347], [705, 259], [676, 259], [702, 358], [698, 360], [695, 356], [677, 289], [675, 289], [673, 309], [667, 328], [667, 357], [665, 357], [665, 337], [653, 350], [643, 353], [634, 348], [626, 336], [623, 335], [622, 362], [621, 324], [615, 300], [614, 271], [604, 271], [603, 269], [614, 239], [615, 250], [617, 250], [619, 226], [625, 224], [625, 221], [619, 219], [619, 212], [615, 213], [614, 221], [581, 221], [579, 219], [579, 212], [575, 212], [574, 221]],
      walkTo: [596, 378], face: "E", look: twice("rome.forum.site.look", "rome.forum.site.look2"), use: "rome.forum.site.use" },
    { id: "crane", name: "crane", verb: "Touch", poly: [[605, 35], [599, 42], [599, 53], [603, 59], [609, 62], [599, 160], [592, 161], [588, 168], [588, 195], [636, 195], [636, 168], [631, 161], [625, 160], [620, 96], [650, 202], [649, 204], [638, 204], [627, 213], [619, 229], [614, 248], [612, 294], [619, 327], [619, 364], [626, 364], [626, 343], [631, 350], [640, 355], [650, 355], [656, 352], [662, 345], [663, 360], [670, 360], [669, 331], [677, 302], [695, 362], [704, 361], [704, 352], [691, 308], [693, 306], [701, 309], [701, 304], [688, 297], [674, 240], [692, 240], [737, 340], [743, 350], [748, 350], [751, 347], [751, 342], [634, 79], [642, 86], [797, 286], [799, 286], [799, 279], [648, 85], [662, 96], [795, 227], [799, 227], [799, 223], [625, 52], [625, 42], [619, 35]],
      walkTo: [610, 420], face: "E", look: "rome.forum.crane.look", use: "rome.forum.crane.use" },
    // ---- in the square: three honorary statues on their columns (one word for all three), Phyllis's garlands, the spring,
    // the stone ring, the moneychanger's table
    { id: "statues-3", name: "statue", plane: "statue-3", poly: [[351, 161], [351, 166], [356, 172], [356, 186], [351, 187], [351, 192], [355, 197], [354, 268], [349, 269], [349, 295], [371, 295], [372, 269], [367, 267], [367, 196], [369, 194], [369, 187], [365, 186], [364, 161]],
      walkTo: [395, 295], face: "W", look: "rome.forum.statues.look" },
    { id: "statues-2", name: "statue", plane: "statue-2", poly: [[520, 133], [519, 138], [525, 146], [524, 164], [521, 165], [521, 174], [523, 176], [523, 275], [521, 277], [515, 277], [515, 307], [517, 309], [545, 309], [545, 278], [540, 278], [538, 276], [537, 176], [542, 170], [542, 165], [537, 165], [535, 163], [534, 134], [527, 133], [525, 135], [524, 133]],
      walkTo: [500, 312], face: "E", look: "rome.forum.statues.look" },
    { id: "statues", name: "statue", plane: "statue-1", poly: [[267, 112], [261, 112], [258, 116], [256, 113], [250, 113], [250, 118], [258, 128], [257, 153], [248, 154], [248, 160], [251, 160], [253, 165], [256, 167], [255, 287], [253, 292], [244, 292], [244, 332], [278, 332], [283, 329], [283, 290], [275, 291], [273, 287], [273, 167], [276, 164], [275, 154], [271, 153], [270, 148], [270, 119]],
      walkTo: [316, 334], face: "W", look: "rome.forum.statues.look" },
    { id: "garlands", name: "garlands", verb: "Touch", poly: [[216, 355], [215, 361], [221, 363], [221, 374], [214, 379], [214, 388], [219, 392], [219, 397], [223, 397], [225, 392], [229, 393], [228, 399], [230, 405], [234, 408], [234, 413], [238, 413], [239, 408], [242, 408], [241, 426], [215, 426], [210, 429], [210, 440], [213, 450], [220, 452], [242, 452], [241, 454], [233, 454], [230, 462], [222, 466], [222, 471], [244, 476], [271, 475], [281, 472], [281, 465], [263, 462], [259, 454], [250, 453], [250, 392], [260, 387], [260, 394], [266, 400], [266, 405], [270, 405], [271, 401], [278, 400], [281, 395], [281, 389], [272, 382], [272, 363], [277, 361], [277, 356], [251, 356], [249, 346], [242, 347], [241, 356]],
      walkTo: [232, 492], face: "W", look: "rome.forum.garlands.look", use: "rome.forum.garlands.use" },
    { id: "spring", name: "spring", poly: [[144, 440], [0, 441], [0, 509], [114, 509], [143, 481]],
      walkTo: [64, 524], face: "N", look: "rome.forum.spring.look", use: "rome.forum.spring.use", useWith: { coin: "rome.forum.spring.coin" } },
    { id: "puteal", name: "stone ring", verb: "Step on", poly: [[336, 353], [336, 361], [338, 362], [338, 380], [336, 382], [336, 387], [417, 387], [417, 382], [415, 380], [415, 362], [417, 361], [417, 353], [414, 351], [391, 348], [364, 348], [345, 350]],
      walkTo: [308, 391], face: "E", look: "rome.forum.puteal.look", use: "rome.forum.puteal.use" },
    { id: "table", name: "moneychanger's table", verb: "Touch", poly: [[409, 303], [410, 331], [413, 332], [413, 355], [410, 356], [410, 376], [413, 377], [414, 400], [421, 400], [421, 378], [423, 376], [431, 376], [433, 378], [433, 392], [437, 392], [439, 389], [440, 376], [453, 376], [454, 389], [456, 389], [457, 392], [462, 391], [463, 376], [476, 376], [477, 394], [479, 396], [479, 400], [486, 400], [486, 378], [491, 376], [491, 361], [487, 356], [483, 355], [483, 332], [493, 331], [493, 318], [488, 303], [484, 303], [483, 301], [477, 301], [476, 303], [420, 303], [419, 301], [413, 301], [412, 303]],
      walkTo: [518, 401], face: "W", look: "rome.forum.table.look", use: "rome.forum.table.use",
      useWith: { coin: "rome.forum.table.coin", quarter: "rome.forum.table.quarter" } },
    // ---- the pigeons: each of the seven near birds is a thing to click, its area going with it (see the top of the file).
    // Put away until the first bird is found for each (a few tenths of a second after the scene is built).
    ...Array.from({ length: BIRDS }, (_, n) => ({ id: n ? `pigeons-${n + 1}` : "pigeons", ...pigeons, pigeon: true, away: true, when: () => false,
      poly: [[400, 500], [410, 500], [410, 510], [400, 510]] })),
    // ---- the people. Each one's area is traced round the figure the game draws on the mark, two pixels outside it (the
    // Gaul facing the hoarding, without his shadow; Phyllis seated, her stool and her skirt), and goes with them on their walks.
    {
      id: "phyllis", name: "garland seller", verb: "Talk to", poly: [[176, 409], [192, 409], [195, 423], [200, 435], [201, 447], [209, 453], [210, 471], [214, 477], [214, 489], [173, 489], [172, 471], [170, 459], [169, 441], [171, 423]], walkTo: AT_PHYLLIS, face: "W",
      look: (g) => (g.flag("rome.hasLamp") ? g.say("rome.phyllis.look3") : twice("rome.phyllis.look", "rome.phyllis.look2")(g)),
      use: talkToPhyllis,
      useWith: { coin: talkToPhyllis, quarter: talkToPhyllis, lamp: talkToPhyllis, gaultoga: "rome.phyllis.gaultoga", toga: "rome.phyllis.toga", breakfast: "rome.phyllis.breakfast" },
    },
    {
      id: "gaul", name: "Gaulish senator", verb: "Talk to", poly: [[642, 318], [657, 318], [658, 326], [660, 338], [665, 350], [659, 356], [659, 374], [655, 380], [654, 386], [657, 394], [658, 404], [641, 404], [643, 394], [644, 386], [641, 374], [639, 362], [639, 344], [641, 332]], walkTo: AT_GAUL, face: "E",
      when: (g) => !g.flag("rome.swapped"),
      look: twice("rome.gaul.look", "rome.gaul.look2"), use: talkToGaul,
      useWith: {
        gaultoga: talkToGaul,
        toga: "rome.gaul.toga", coin: "rome.gaul.coin", quarter: "rome.gaul.quarter", phone: "rome.gaul.phone", gum: "rome.gaul.gum",
        breakfast: "rome.gaul.breakfast", incense: "rome.gaul.incense", lamp: "rome.gaul.lamp",
      },
    },
  ],

  // Runs as the scene is built, and after a save is loaded: the pigeons' areas go with the pigeons, and the crane's wheel
  // turns now and then.
  setup(g) {
    followPigeons(g);
    craneLife(g);
  },

  // Runs when the lead arrives. It must be safe to run twice, so it checks its own fact.
  // From the steps he arrives at the far end, small, at the foot of Saturn's steps, and walks a good way down the square;
  // from the river he comes out of the Tuscan street's mouth onto the square. The first time, he looks about him: the
  // Forum, his own temple way down at the end, the gold roof on the hill (rome.sawForum).
  async enter(g, from) {
    if (from === "rome-steps") await g.walkTo(DOWN_THE_SQUARE[0], DOWN_THE_SQUARE[1]);
    else if (from === "rome-tiber") await g.walkTo(OUT_OF_THE_STREET[0], OUT_OF_THE_STREET[1]);
    if (g.flag("rome.sawForum")) return;
    const me = g.lead;
    await g.wait(350);
    if (me) me.face("S");                                         // to us: it is everything at once
    await g.say("rome.forum.arrive.1");
    if (me) me.face("N");                                         // and back up the square to the far end, where he came in
    await g.say("rome.forum.arrive.2");
    if (me) me.look(280, 80);                                     // and up, at the hill and its gold roof
    await g.say("rome.forum.arrive.3");
    g.flag("rome.sawForum", true);
  },
};

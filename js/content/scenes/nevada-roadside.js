// Act Four, at the roadside: the middle of Nevada, the next morning, where the phone was last seen. Grandpa Joe's Last
// Stop. Mom, Big Sister and Little Sister play, and the player switches between them. The store is a scene of its own
// (nevada-store, through the shop's door on the porch): the three go in and out of it together.
//
// NEVADA-12SA (round twelve, SCENES-12: briefs/out/nevada-expansion-design.md, the act as expanded). The chains, and the
// gate, and each of the three doing what only she can:
//   Mom asks Grandpa Joe nicely (#5, a dialogue tree: joeTree), and he tells what he saw          (chain A)
//   ...the coin that fell out of the sky is Ranger's, and Ranger trades: Big Sister holds out the mirror shades Mom
//      bought in the store, flat on both hands, and he gives her the coin, warm (#10: rangerTree)  (chain A)
//   ...and she reads it there and then (#6)                                                        (chain A)
//   Little Sister asks the man in gray so many questions that he steps aside (#7)                 (chain B)
//   ...and Big Sister reads the notice he was standing in front of (#8)                            (chain B)
//   (in the store, Little Sister and Grandma Jolene's hens (#11): the run of the store, and the window)  (chain C)
//   the middle: whoever holds the coin flashes the morning sun off it, onto the place where the tracks stop (#9); a door
//      the size of the coin; the closing scene of the old act, word for word ("Some when"); then her head in the hole,
//      and Big Sister's rule: a bigger shine, a bigger door
//   the letterbox: through the little door, the Son, in Rome (letterboxTree, held through the door); a penny for luck
//      (LETTER-17: rewritten: Mom hears her son, on her knees at the door, and he explains until she understands that he
//      is in another time; his warning, and her answer; Grandpa Joe, who heard it all; Ranger brings her the handbag)
//   #12: a bigger shine. Mom's car never shone; the banjo is a half-answer (a door the size of a banjo, while he plays);
//      the sun shade from Jolene's window, held by Grandpa Joe in the low sun, opens a door as wide as a windshield
//   the gate (#13): the goodbyes, and they go through, hand in hand; then the cut-scene "Backup" (SCENES-12C)
//
// The coin is the one the Son threw through the door in Rome: what goes into a door in one year comes out of one in
// another. And where the tire tracks stop there is a door too: shut, invisible, humming. Light opens a door, and the
// more light, the bigger the door. Grandpa Joe saw it happen and does not know what he saw: the low sun flashed off the
// wagon's chrome, and the sky opened where the flash fell. The family do with a new silver coin what the wagon did by
// accident: a coin's worth of light, a coin's worth of door. Then a banjo's worth, and then a windshield's.
//
// The family's faith hangs on moments that were already here, and no puzzle knows of it (briefs/WEAVE.md):
//   the coin, when Big Sister reads it, is the coin of the tribute money, and Mom has the verse (Matthew 22:21)
//   before the coin goes up, Mom bows her head and the girls with her: a prayer in a line, and Little Sister's Amen
//   just before the reveal Little Sister asks what B.C. is, and is told
//   after "Daddy's EARLY", which stays the top of the scene, Mom has Psalm 31:15, and then the last two lines as they were
//   at the walk through, Grandpa Joe has the first half of Psalm 121:8 and Mom the second, as they said it at their own
//   front door the night before (LETTER-17: after his promise, "Porch light on. However long it takes."; and she no
//   longer says the reference)
// And Little Sister's flashlight, which comes in her pocket from the house, gets its own answer where the tracks stop.
//
// The author's two rules of 7 October (briefs/DATING.md) hang on moments that were already here as well:
//   the years: the notice seals sectors 44 and 1921, every year before Christ is the Bible's own count, and 1921 B.C.
//     is on Big Sister's timeline, the year Abram went down into Egypt. Her mother knows the chapter. Big Sister sees,
//     once, that the doors open on years that matter, and does not know why.
//   the chickens: Jolene's hens (out back, seen from the store) have stopped laying and face the fence; at the door it
//     is Little Sister who hears chickens, before anybody smells a sausage; and once she has heard of the hens, she
//     misses General Feathers.
//
// Try it: index.html?scene=nevada-roadside&lead=mom
// (later states: &flags=nevada.arrived,nevada.witness,nevada.traded,nevada.coinRead,nevada.distracted,nevada.notice,nevada.connected,
//  nevada.jolene,nevada.shadeGiven,nevada.doorOpen,nevada.heardSon; the things they carry are given by script: game.give("coin").)

import { joeTree, rangerTree, letterboxTree } from "../talk/nevada.js";

const art = "art/scenes/nevada-roadside/";

const each = (id) => ({ mom: `${id}.mom`, bigsis: `${id}.bigsis`, lilsis: `${id}.lilsis` });
const who = (g) => g.store.data.active;
/** Has this line been spoken yet? (The engine counts every line it says.) */
const heard = (g, id) => !!g.store.data.seenLines[id];
/** Does Big Sister hold both halves of the answer: what the coin is, and what the notice says? */
const ready = (g) => !!(g.flag("nevada.coinRead") && g.flag("nevada.notice"));
/** Head bowed, hands folded (Figure.pray in the engine). It is for someone standing still: let it go before she walks or reaches. */
const pray = (a, on) => a && a.pray && a.pray(on);
const THREE = ["mom", "bigsis", "lilsis"];
/** Grandpa Joe is holding the sun shade to the sun at the glass: from #12 until the cut-scene takes over. */
const holding = (g) => !!g.flag("nevada.wideOpen") && !g.flag("nevada.backup");
/** The family has gone through the door (#13). */
const gone = (g) => !!g.flag("nevada.left");
/** How big someone is with their feet at row y: the scene's own depth (horizon 290, full 590), as the engine works it out. */
const sizeAt = (y) => Math.min(1.12, Math.max(0.26, (y - 290) / 300));
const far = (a, [x, y]) => !a || Math.hypot(a.x - x, (a.y - y) * 2.2) > 30;

/** Once Big Sister has both the coin and the notice, she puts them together. Said once. */
async function connect(g) {
  if (ready(g) && !g.flag("nevada.connected")) {
    await g.say("nevada.connect");
    g.flag("nevada.connected", true);
  }
}

// ---------- where people stand ----------
// Every place here was set against the picture with the people standing in it (round twelve's measurements are the
// painter's: art/scenes/nevada-roadside/layout.json, and S/work-paintA/ready.md).
const JOE = [388, 498];                       // his rocking chair (the old-timer's place, kept: the rocker stands on the ground in front of the porch, in the sun)
const RANGER = [352, 512];                    // Ranger, sitting up on the ground beside the chair, on our side of it
const STORE = [261, 450];                     // in front of the shop's door, on the porch (the painter's stand place for `store`)
const JOLENE_IN = [262, 446], JOLENE_OUT = [270, 458];          // Jolene in the doorway, and a step out onto the porch (#13)

// ---------- the light ----------
// The door in time is where the tracks stop, in the air over the patch of fused sand: a ripple in the paint, the size of
// a coin (round ten: the engine's `portal`, in `fx` below), shut and unseen until the flash opens it. The light is drawn
// live (see `live` below): `#glint` is the spot of reflected sunlight, `#ray` the faint beam to it, `#spark` the flash of
// the coin itself, `#burst` the banjo's chrome catching the sun, and `#sheen` the halo round the sun shade's flash.
const PLACE = [646, 483];                                         // the painter's `over_the_glass`: where it hums
// Where they stand for the flash. (The painter's marks "at the glass" put the three of them shoulder to shoulder, which
// suits one picture and not this scene: words go over a speaker's head, and Little Sister's head is lower than her
// mother's shoulder, so in a huddle whatever she says is written across the other two's faces. So the one with the coin
// stands alone at the near corner of the glass, an arm's length from the place; the two tall ones watch from the left;
// and Little Sister ends up beside the door, where her words sit clear above their heads.)
// NEVADA-12SA: the two tall ones watch from a row further back than they did (it was 444, 590 and 488, 592). Grandpa Joe
// sits in his rocker behind them now, and words go over a speaker's head: from the front row, everything Mom and Big
// Sister said through the flash was written across his face. From here their words pass over his hat, and Little Sister's
// are lifted with theirs (the engine lifts a small speaker's words clear of a tall head beside her).
const HOLD = [572, 560];                                          // whoever has the coin; and later Grandpa Joe, with the banjo, and with the shade
const BACK = { mom: [474, 552], bigsis: [522, 546], lilsis: [536, 580] };
const EYE = [616, 570];                                           // Little Sister, with her eye to the door: it is at the height of her eye
const HEAD = [642, 566];                                          // her head in the hole: up under it, her face at it
// Mom lifts her out: Mom beside her, and she a step back. (NEVADA-12SA: the little door is used after this, and whoever
// of the three is standing in front of it covers it with herself, so both stand clear of it, to its left; it was 612, 578
// and 626, 582. They keep off the place to talk into it from, too (DOORSIDE, below), or whoever comes to talk is put
// beside them, right in front of it. Little Sister steps back here, too, when she has posted her penny.)
const LIFT = { mom: [604, 556], lilsis: [586, 592] };
const DOORSIDE = [600, 574];                                      // whoever speaks into the little door
const POST = [624, 568];                                          // Little Sister posting her penny into it (it is at the height of her eye)
const HANDOFF = [532, 568];                                       // whoever has the sun shade hands it to Grandpa Joe here, at the corner of the glass
const ASIDE = { mom: [520, 590], bigsis: [494, 574], lilsis: [546, 584] };     // off the corner of the glass, when he comes to stand there
// In front of the wide door, in a row, hand in hand, Little Sister in the middle (#13); and where each goes into it.
const LINE = { mom: [604, 588], lilsis: [630, 588], bigsis: [656, 583] };
const INTO = { mom: [634, 553], lilsis: [646, 555], bigsis: [658, 553] };

/** Where the coin is when one of them holds it out toward the place: in her hand, at the end of her arm.
    (Measured on each of them reaching: so far along, and so far up, as a share of her height.) */
const REACH = { mom: [0.37, 0.64], bigsis: [0.37, 0.64], lilsis: [0.37, 0.62] };
function hand(g) {
  const me = g.lead, tall = me.h * me.scale, [along, up] = REACH[me.id] || REACH.mom;      // (she is facing east: her arm is out to the right)
  return [me.x + along * tall, me.y - up * tall];
}
/** Where the chrome of Grandpa Joe's banjo catches the sun, on the picture: the tuning pegs at the end of its neck, which
    stands out clear of him, up and to his left as we look (in the rocker), or out toward the glass (on his feet, facing
    the sun). Measured on him as the game draws him, as a share of his height from his feet. (The light is drawn under the
    people, like the coin's spark: at the white head of the banjo, in his lap, he hid all of it.) */
function banjoAt(joe) {
  const tall = joe.h * joe.scale, [along, up] = joe.kind === "grandpajoe-play" ? [0.45, 0.736] : [0.537, 0.727];
  return [joe.x + along * tall, joe.y - up * tall];
}
/** Put the spot of light at a place, with its beam from where the flash comes from. */
function aim(g, from, x, y) {
  const glint = g.q("#glint"), ray = g.q("#ray");
  if (glint) glint.setAttribute("transform", `translate(${x} ${y})`);
  if (ray) ray.setAttribute("points", `${from[0]},${from[1]} ${x - 1},${y - 4} ${x + 1},${y + 4}`);
}
/** Show or hide the parts of the flash: the coin's own spark, the beam, the spot where it lands, the banjo's burst, the shade's sheen. */
function shine(g, { spark = 0, ray = 0, glint = 0, burst = 0, sheen = 0 } = {}, from = null) {
  const set = (id, opacity) => { const el = g.q(id); if (el) el.setAttribute("opacity", opacity); };
  set("#spark", spark); set("#ray", ray); set("#glint", glint); set("#burst", burst); set("#sheen", sheen);
  if (from) g.q("#spark")?.setAttribute("transform", `translate(${from[0]} ${from[1]})`);
}
const light = (g, id, opacity) => { const el = g.q(id); if (el) el.setAttribute("opacity", opacity); };

// ---------- the door's three sizes ----------
// Two of the engine's portals (`fx` below). `door` is the coin's, r 10, as it has been since round ten. `wide` is the
// windshield's: its middle where the coin's is, r 66 and 0.45 as wide as it is tall, so that wide open it stands from the
// sand at row 556 to row 410 (higher than Mom's head where she stands in front of it) and is as wide as the two girls
// side by side. Round, at a third of that, it is the banjo's (r 25: bigger than a coin, smaller than a girl). The wide
// one lies over the coin's, so as it grows the coin's door is inside it, and as it shuts the coin's is there again.
const SIZES = {
  shut: { coin: 0, wide: 0 },
  coin: { coin: 1, wide: 0 },
  banjo: { coin: 1, wide: 1, scale: 0.34, shape: 1 },
  wide: { coin: 1, wide: 1, scale: 1, shape: 0.45 },
};
/** How far open each of the two portals is, and the wide one's size and shape, between two sizes (k from 0 to 1). */
function between(from, to, k) {
  const lerp = (a, b) => a + (b - a) * k;
  const shape = from.wide > 0 && to.wide > 0 ? { scale: lerp(from.scale, to.scale), shape: lerp(from.shape, to.shape) }
    : to.wide > 0 ? { scale: to.scale, shape: to.shape } : { scale: from.scale, shape: from.shape };      // (opening, it has its new size at once and grows from nothing; shutting, it keeps its own)
  return { coin: lerp(from.coin, to.coin), wide: lerp(from.wide, to.wide), ...shape };
}
function put(g, s) {
  const c = g.effects.get("door"), w = g.effects.get("wide");
  if (c) c.open(s.coin);
  if (w) w.open(s.wide, { scale: s.scale ?? 1, wide: s.shape ?? 0.45 });
}
/** The door in time, to one of its sizes ("shut", "coin", "banjo", "wide") over `ms` (at once with none). For this scene's
    scripts, its `setup`, and the cut-scene "Backup" (which calls g.scene.door(g, "shut", 900) when Grandpa Joe lets the
    shade down). Shutting from wide open, it folds from the outside in: to the coin, then to nothing. */
async function sizeDoor(g, size, ms = 0) {
  const to = SIZES[size], c = g.effects.get("door"), w = g.effects.get("wide");
  if (!to) { console.warn(`The door in time has no size called "${size}": shut, coin, banjo or wide.`); return; }
  if (!c || !w) return;
  w.refresh();                                                    // (the paint it bends as it is now: the shade in his hands, or not)
  const from = { coin: c.isOpen, wide: w.isOpen, scale: w.opts.scale, shape: w.opts.wide };
  if (to.coin === 0 && from.wide > 0 && ms > 0) {                // from wide open to nothing: to the coin first
    await sizeDoor(g, "coin", ms * 0.65);
    return sizeDoor(g, "shut", ms * 0.35);
  }
  if (!(ms > 0)) return put(g, between(from, to, 1));
  await g.tween(ms, (k) => put(g, between(from, to, k)), g.ease.out);
}

// ---------- Grandpa Joe, up and about ----------
const joeOf = (g) => g.actor("grandpajoe");
/** Grandpa Joe gets up out of the rocking chair, slowly, a hand to the small of his back (`back`). The chair stays where it
    is (the engine leaves it on the stage as "grandpajoe.seat"). */
async function getUp(g, { back = true } = {}) {
  const joe = joeOf(g);
  if (!joe || !joe.seated) return joe;
  await joe.sit(false);
  if (back) await joe.fidget("back");
  return joe;
}
/** Draw Grandpa Joe as another state of himself (js/art/people.js), at a place, keeping his id. The engine takes a seat
    away with whoever got up from it, so the rocking chair is put back where it stands. Gives back the figure he was. */
function swapJoe(g, kind, [x, y], face) {
  const cast = g.view.cast, was = joeOf(g), seat = cast.get("grandpajoe.seat");
  if (!was) return null;
  cast.remove("grandpajoe");
  if (seat && !cast.get(seat.id)) cast.add(seat);
  cast.addFigure("grandpajoe", kind, x, y, sizeAt(y)).face(face);
  return was;
}
/** Put back the figure he was (up from his chair, with the chair still his to sit down in), where he stands now. */
function unswapJoe(g, was, face) {
  const cast = g.view.cast, now = joeOf(g), seat = cast.get("grandpajoe.seat");
  if (!was) return null;
  const [x, y] = now ? [now.x, now.y] : [was.x, was.y];
  cast.remove("grandpajoe");
  if (seat && !cast.get(seat.id)) cast.add(seat);
  cast.add(was);
  was.place(x, y, sizeAt(y)).face(face);
  return was;
}
/** Back to his chair, and down into it. */
async function sitDown(g) {
  const joe = joeOf(g);
  if (!joe || joe.seated || !joe.standAt) return;
  const [x, y] = joe.standAt;
  await g.walkTo(x, y, "grandpajoe");
  await joe.sit(true);
}
/** Anyone of the three standing on the corner of the glass, where he is coming to stand, steps aside; and anyone standing
    in front of the door, where it is going to grow (whoever stood there would hide it: she is nearer than it is). */
async function clearHold(g) {
  const there = THREE.filter((id) => {
    const a = g.actor(id);
    return a && a.opacity > 0 && ((Math.abs(a.x - HOLD[0]) < 46 && Math.abs(a.y - HOLD[1]) < 22) || (a.x > 600 && a.x < 700 && a.y > 540));
  });
  await Promise.all(there.map((id) => g.walkTo(ASIDE[id][0], ASIDE[id][1], id)));
}

// ---------- the banjo: the Last Stop Rag, his own, and in the low sun it flashes ----------
/** He plays while `playing.on`: a pass of his strum at a time (the rig's `strum`), and a phrase of the tune with each
    (sound.js `banjo`), and the chrome catching the sun now and then. (While he talks the strum waits.) */
async function playOn(g, playing) {
  let n = 0;
  while (playing.on && !g.clock.skipping) {
    const joe = joeOf(g);
    if (!joe || joe.talking || joe.walking || joe.act || joe.move) { await g.wait(150); continue; }
    g.sfx("banjo");
    const pass = joe.fidget("strum");
    if (n++ % 2 === 1) twinkle(g, banjoAt(joe));                  // (every other pass, from the second: a script may flash it itself first)
    await pass;
    if (!joe.fid) await g.wait(30);                              // (a strum that could not start: never a loop with no wait in it)
  }
}
/** The chrome catching the low sun: a burst of light round the banjo, there and gone. */
async function twinkle(g, at) {
  const el = g.q("#burst");
  if (!el) return;
  el.setAttribute("transform", `translate(${at[0]} ${at[1]})`);
  await g.tween(140, (k) => el.setAttribute("opacity", k), g.ease.out);
  await g.wait(180);
  await g.tween(360, (k) => el.setAttribute("opacity", 1 - k));
}

// ---------- the dialogue trees (js/content/talk/nevada.js), and the hooks that stage them ----------
/** joeTree's `lemonade`: Mom has bought three lemonades. He gets up, pours three at the stand (it is beside his chair), and sits back down. */
async function lemonade(g) {
  const joe = await getUp(g, { back: false });
  if (!joe) return;
  joe.face("NE");
  for (let n = 0; n < 3; n++) await joe.play(g.clock, "reach");
  await sitDown(g);
  joeOf(g)?.face("SE");
}
/** joeTree's `witness`: the right car is named and the story told. He looks up the road toward the glass, a hand to his hat. */
async function witness(g) {
  const joe = joeOf(g);
  if (!joe) return;
  joe.face("E");
  await joe.fidget("hat");
  await g.wait(250);
  joe.face("SE");
}
/** joeTree's `coinTold`: "He don't steal. He trades." He tips his hat (the dent), and Ranger, sitting up with his hands
    folded, looks at Mom. */
async function coinTold(g) {
  const joe = joeOf(g), r = g.actor("ranger"), mom = g.actor("mom");
  if (r && mom) r.look(mom.x, mom.y);
  if (joe) await joe.fidget("hat");
  if (r) await r.play(g.clock, "look", { ms: 900 });
}
/** joeTree's `play`: Little Sister has asked for a tune. He plays a few bars of the Last Stop Rag in his rocker, in the low
    sun (the porch's roof shades the boards behind him, not the chair), and the chrome of the banjo flashes. */
async function play(g) {
  const joe = joeOf(g);
  if (!joe || !joe.seated) return;
  joe.face("SE");
  const playing = { on: true }, tune = playOn(g, playing);
  await g.wait(4600);
  playing.on = false;
  await tune;
}
let banjoNow = null;                                            // while he plays at the glass: { on, tune, was }
/** joeTree's `banjo`: #12's half-answer. He gets up, walks to the glass, and plays facing the sun: the low sun comes off
    the banjo, onto the place, and the door grows from a coin to a banjo, and stays that size while he plays. */
async function banjo(g) {
  const joe = await getUp(g);
  if (!joe) return;
  await clearHold(g);
  await g.walkTo(HOLD[0], HOLD[1], "grandpajoe");
  const was = swapJoe(g, "grandpajoe-play", HOLD, "SE");         // on his feet, the banjo across him to play
  const playing = { on: true };
  banjoNow = { playing, was, tune: playOn(g, playing) };
  await g.wait(600);
  // the flash, the beam onto the place, and a banjo's worth of door
  const from = banjoAt(joeOf(g));
  g.q("#burst")?.setAttribute("transform", `translate(${from[0]} ${from[1]})`);
  aim(g, from, PLACE[0], PLACE[1]);
  await g.tween(220, (k) => shine(g, { burst: k, ray: 0.45 * k, glint: k }), g.ease.out);
  g.sfx("portal");
  await Promise.all([sizeDoor(g, "banjo", 1100), g.tween(900, (k) => shine(g, { burst: 1 - k, ray: 0.45 * (1 - k), glint: 1 - k }))]);
  shine(g);
  for (const id of THREE) { const a = g.actor(id); if (a) a.look(PLACE[0], PLACE[1]); }
}
/** joeTree's `banjoDone`: he stops; the door shuts back to a coin, and the music with it; he walks back and sits down. */
async function banjoDone(g) {
  const now = banjoNow;
  banjoNow = null;
  if (now) { now.playing.on = false; await now.tune; }
  await sizeDoor(g, "coin", 700);
  if (now) unswapJoe(g, now.was, "W");
  await sitDown(g);
  joeOf(g)?.face("SE");
}
/** joeTree's `hold`, and the end of the shade taken to the glass or given to him: #12's answer. He gets up out of the
    rocker, slowly, a hand to the small of his back; whoever has the sun shade hands it to him at the corner of the glass
    (anyone standing there steps aside); he holds it square to the sun, and the door grows from the coin outward to a
    windshield's width. Sets nevada.wideOpen: from then on `setup` draws all of it from the facts. */
async function hold(g) {
  const giver = THREE.find((id) => (g.store.data.inventory[id] || []).includes("storeshade")) || null;
  await getUp(g);
  await clearHold(g);
  const hands = giver ? g.actor(giver) : null;
  await Promise.all([g.walkTo(HOLD[0], HOLD[1], "grandpajoe"), hands && far(hands, HANDOFF) ? g.walkTo(HANDOFF[0], HANDOFF[1], giver) : null]);
  if (hands) {
    const joe = joeOf(g);
    hands.face("E");
    if (joe) joe.face("W");
    await hands.play(g.clock, "reach");
  }
  takeFrom(g, "storeshade");                                      // (it stays with him: the family never has it again)
  swapJoe(g, "grandpajoe-shade", HOLD, "E");                       // up it goes, square to the sun
  g.flag("nevada.wideOpen", true);                                 // (and the shade is in his hands: its cut-out's `when`)
  // A windshield's worth of flash, and a windshield's worth of door: it opens from the coin outward.
  aim(g, [660, 452], PLACE[0], PLACE[1]);
  g.sfx("flash");
  await g.tween(260, (k) => shine(g, { sheen: k, glint: k }), g.ease.out);
  g.sfx("portal");
  await sizeDoor(g, "wide", 1800);
  await g.tween(800, (k) => shine(g, { sheen: 1 - k, glint: 1 - k }));
  shine(g);
  if (hands) hands.look(PLACE[0], PLACE[1]);
}
/** A thing taken from whichever of the three is carrying it (g.take takes only from the one being played). */
function takeFrom(g, item) {
  const d = g.store.data, holder = g.holder(item);
  if (!holder) return null;
  if (holder === d.active) g.take(item);
  else { const pockets = d.inventory[holder]; pockets.splice(pockets.indexOf(item), 1); g.store.emit(); }
  return holder;
}

/** The sun shade, taken to the glass (or given to Grandpa Joe) instead of asked for in his talk: the same, with the lines
    the tree says before it and after it. Before the coin has opened the little door it is too soon (#12 needs #9), and
    before they have heard who is on the other side of it (the letterbox), the little door comes first. */
async function shadeToGlass(g) {
  const me = who(g);
  if (!g.flag("nevada.doorOpen")) return g.say(ready(g) ? `nevada.shade.early.${me}` : `nevada.tracks.early.${me}`);
  if (!g.flag("nevada.heardSon")) return g.say(`hint.nevada.letterbox.${me}`);
  await g.say("nevada.shade.need", "nevada.shade.ask", "nevada.shade.joe");
  await hold(g);
  await g.say("nevada.shade.open.lilsis", "nevada.shade.open.bigsis", "nevada.shade.open.mom");
}
async function shadeToJoe(g) {
  if (!g.flag("nevada.doorOpen")) return g.say(g.fallback("nope"));
  return shadeToGlass(g);
}

const JOE_TREE = joeTree({ lemonade, witness, coinTold, play, banjo, banjoDone, hold });
// Three things the tree offers that this scene holds back, so that what is said is true where he is (each `when` is the
// tree's own, and something more): while he holds the sun shade his hands are full, so he is not asked for the banjo, or
// to play it; and he holds the shade only once they have heard the Son through the little door (the beat nevada.shade
// needs nevada.heardSon: the Son's warning comes before they go through).
const also = (tree, node, id, more) => {
  const o = tree.nodes[node] && tree.nodes[node].options.find((x) => x.id === id);
  if (o) { const own = o.when; o.when = (g) => (!own || own(g)) && more(g); }
};
also(JOE_TREE, "after", "banjo", (g) => !holding(g));
also(JOE_TREE, "lil", "banjoLil", (g) => !holding(g));
also(JOE_TREE, "big", "banjoBig", (g) => !holding(g));
also(JOE_TREE, "lil", "play", (g) => !holding(g));
also(JOE_TREE, "after", "hold", (g) => !!g.flag("nevada.heardSon"));

/** Grandpa Joe, talked to: his tree (#5, Ask Nicely, and everything after). */
async function talkToJoe(g) {
  await g.talk(JOE_TREE);
  const joe = joeOf(g);
  if (joe && joe.seated) joe.face("SE");
}

// ---------- Ranger: the trade (#10) ----------
/** rangerTree's `trade`, and the mirror shades used on him by Big Sister: she holds them out flat on both hands and keeps
    still; he takes them, turns them over (reading them with his paws), looks at himself in both lenses, scampers into
    the store for his half of the bargain (his basket is under the counter) and back, and puts the coin in her hand,
    warm; then he puts the shades on. He wears them for the rest of the game (the `shades` set of his frames). */
async function trade(g) {
  const r = g.actor("ranger"), me = g.lead;
  if (r && me) r.look(me.x, me.y);
  if (me) me.hold(true);                                          // both hands out, flat, and very still
  await g.wait(700);
  if (r) await r.play(g.clock, "reach");                          // he takes them
  g.take("mirrorshades");
  if (me) me.hold(false);
  if (r) {
    await r.play(g.clock, "wash", { ms: 1600 });                  // turns them over in his paws
    await r.play(g.clock, "look", { ms: 900 });                   // himself, in both lenses
    await fetchCoin(g, r);                                        // into the store, and back
    if (me) r.look(me.x, me.y);
    await r.play(g.clock, "reach");                               // the coin, in her hand
  }
  g.give("coin");                                                 // (to the one being played: Big Sister, who is talking to him)
  if (r) r.variant("shades");                                     // and the shades go on
  g.flag("nevada.traded", true);
  if (r) await r.play(g.clock, "look", { ms: 700 });
}
/** Ranger scampers into the store, and back out with something. */
async function fetchCoin(g, r) {
  await r.sit(false);
  r.hurry = true;
  await g.walkTo(STORE[0] + 4, STORE[1] + 2, "ranger");
  await g.tween(220, (k) => r.fade(1 - k));
  await g.wait(900);
  await g.tween(220, (k) => r.fade(k));
  r.hurry = true;
  await g.walkTo(RANGER[0], RANGER[1], "ranger");
  await g.moveTo(RANGER[0], RANGER[1], "ranger");                // (the walk ends at the edge of the chair's patch of ground: the last step onto his place)
  await r.sit(true);
}
/** rangerTree's `tail`: he turns round and shows her his tail. */
async function tail(g) {
  const r = g.actor("ranger"), me = g.lead;
  if (!r) return;
  r.face(me && me.x < r.x ? "E" : "W");
  await g.wait(600);
}
/** rangerTree's `snatch`: Little Sister holds the mirror shades out; he reaches; she snatches them back. */
async function snatch(g) {
  const r = g.actor("ranger"), me = g.lead;
  if (r && me) r.look(me.x, me.y);
  if (me) me.hold(true);
  await g.wait(500);
  const reach = r ? r.play(g.clock, "reach") : Promise.resolve();
  await g.wait(280);
  if (me) me.hold(false);
  await reach;
}
const RANGER_TREE = rangerTree({ trade, tail, snatch });
// The trade is offered once they know what he has (#10 needs #5: Grandpa Joe has told them the coin is Ranger's).
also(RANGER_TREE, "big", "trade", (g) => !!g.flag("nevada.witness"));

/** If Big Sister has just traded for the coin, she reads it there and then (#6: the two beats fall together). */
async function readIfHers(g) {
  if (g.flag("nevada.traded") && !g.flag("nevada.coinRead") && who(g) === "bigsis" && g.has("coin")) await readCoin(g);
}
/** Ranger, talked to: his tree. He looks at whoever is talking; afterward he turns back as he sits. */
async function talkToRanger(g) {
  const r = g.actor("ranger"), me = g.lead;
  if (r && me) r.look(me.x, me.y);
  await g.talk(RANGER_TREE);
  if (r) r.face("SE");
  await readIfHers(g);
}
/** The mirror shades, held out to him: Big Sister trades (once she knows he has the coin), Little Sister snatches them
    back, and Mom draws the line at a raccoon. */
async function shadesToRanger(g) {
  const me = who(g), r = g.actor("ranger");
  if (me === "lilsis") {
    await snatch(g);
    await g.say("nevada.ranger.lil.holder");
    await tail(g);
    await g.say("nevada.ranger.manners");
  } else if (me === "mom") {
    await g.say("nevada.ranger.mom.no", "nevada.ranger.mom.joe");
  } else if (!g.flag("nevada.witness") || g.flag("nevada.traded")) {
    await g.say(g.fallback("nope"));
  } else {
    await g.say("nevada.ranger.fact", "nevada.ranger.method");
    await trade(g);
    await g.say("nevada.ranger.thanks", "nevada.ranger.lil.good", "nevada.ranger.big.fast");
    await readIfHers(g);
  }
  if (r) r.face("SE");
}
/** A penny, offered to him: he sniffs it and hands it back. (He wants to see himself in it.) */
async function pennyToRanger(g) {
  const r = g.actor("ranger"), me = g.lead;
  if (r && me) r.look(me.x, me.y);
  await g.reach();
  if (r) {
    await r.play(g.clock, "reach");
    await r.play(g.clock, "nibble", { ms: 600 });                  // (his nose to it)
    await r.play(g.clock, "reach");
  }
  await g.say("nevada.ranger.copper.joe");
  if (r) r.face("SE");
}

// ---------- chain A: the coin, read ----------
async function readCoin(g) {
  await g.say("nevada.coin.read.1", "nevada.coin.read.2");
  // Caesar's own portrait: it is the coin of the tribute money. Little Sister knows it from Sunday school, Big Sister
  // has the fact, and Mom has the verse. Then back to what matters for the puzzle: the coin is new.
  await g.say("nevada.coin.read.2b", "nevada.coin.read.2c", "nevada.coin.read.2d");
  await g.say("nevada.coin.read.3", "nevada.coin.read.4");
  g.flag("nevada.coinRead", true);
  await connect(g);
}

// ---------- chain B: the man in gray, and what he is standing in front of ----------
async function talkToAgent(g) {
  const me = who(g);
  if (g.flag("nevada.distracted")) return me === "lilsis" ? g.say("nevada.agent.again.1", "nevada.agent.again.2") : g.say("nevada.agent.busy");
  // Mom's second try is General Washington's: courtesy, with the rule book named. It moves him no more than the first.
  if (me === "mom" && heard(g, "nevada.agent.mom.4")) return g.say("nevada.agent.mom.5", "nevada.agent.mom.6", "nevada.agent.mom.7");
  if (me !== "lilsis") return g.say(...[1, 2, 3, 4].map((n) => `nevada.agent.${me}.${n}`));
  // (NEVADA-12SA: "Do you get a snack?" is answered once, to himself, straight after her fifth question: the cheeseburger starts here.)
  await g.say("nevada.agent.lil.1", "nevada.agent.lil.2", "nevada.agent.lil.3", "nevada.agent.lil.4", "nevada.agent.lil.5", "nevada.agent.lil.5b", "nevada.agent.lil.6");
  // He retreats along the fence with a hand to his ear. She goes with him.
  const agent = g.actor("agent");
  agent.face("E");
  await Promise.all([g.moveTo(752, 468, "agent"), g.walkTo(708, 482)]);
  agent.face("E");
  g.lead.face("E");
  g.flag("nevada.distracted", true);
  // (NEVADA-12SA: and the earpiece has a name for him, small and far, which she does not hear and we do: Houston, who is dispatch.)
  await g.say("nevada.agent.lil.7", "nevada.agent.lil.7b", "nevada.agent.lil.8");
}

async function readNotice(g) {
  const me = who(g);
  if (!g.flag("nevada.distracted")) return g.say(`nevada.notice.blocked.${me}`);
  g.closeup(g.art.notice(), "The notice on the fence");
  if (me === "mom") return g.say("nevada.notice.mom.1", "nevada.notice.mom.2");
  if (me === "lilsis") return g.say("nevada.notice.lilsis");
  if (g.flag("nevada.notice")) return g.say("nevada.notice.again");
  await g.say("nevada.notice.big.1", "nevada.notice.big.2", "nevada.notice.big.3");
  g.flag("nevada.notice", true);
  g.closeup();
  await connect(g);
}

// ---------- where the tracks stop ----------

/** Going to the place. Until they know what they are looking at, Mom keeps them off it. After that there is nothing to
    see, and something to hear: whoever goes listens, and remembers what the old man said. Once the little door is open,
    they would like to go through, and cannot (#13's first wrong try); once it is wide, they can. */
async function atTheTracks(g) {
  const me = who(g);
  if (g.flag("nevada.wideOpen")) return goThrough(g);
  if (g.flag("nevada.doorOpen")) return g.say(`nevada.through.small.${me}`);
  if (!ready(g)) return g.say(`nevada.tracks.early.${me}`);
  await connect(g);
  if (heard(g, `nevada.hum.${me}.2`)) return g.say(`nevada.hum.${me}.2`);
  await g.say(`nevada.hum.${me}.1`, `nevada.hum.${me}.2`);
}

/** The coin, used where the tracks stop. */
async function coinAtTheTracks(g) {
  if (g.flag("nevada.wideOpen")) return goThrough(g);
  if (g.flag("nevada.doorOpen")) return g.say("nevada.gate.6");    // it is open already, the size of the coin: the same light will not make it bigger
  return flash(g);
}

/** The coin, held up in the low sun (#9). Whichever of them is holding it does this. */
async function flash(g) {
  const me = who(g);
  if (!ready(g)) return g.say(`nevada.tracks.early.${me}`);
  await connect(g);
  // "Places, girls." The one with the coin goes to the corner of the glass. The other two stand back to watch.
  await g.say("nevada.gate.0");
  const others = THREE.filter((id) => id !== me);
  await Promise.all([g.walkTo(HOLD[0], HOLD[1]), ...others.map((id) => g.walkTo(BACK[id][0], BACK[id][1], id))]);
  for (const id of THREE) { const a = g.actor(id); if (a) a.face("E"); }
  await g.say("nevada.gate.1");
  // First things first. Mom bows her head, and the girls with her: nobody has to be told. A prayer in a line, in
  // her own words, and Little Sister's Amen. Then heads up and hands down, before anyone reaches or walks.
  pray(g.actor("mom"), true);
  await g.wait(280);
  for (const id of ["bigsis", "lilsis"]) pray(g.actor(id), true);
  await g.wait(420);
  await g.say("nevada.pray.1", "nevada.pray.2");
  for (const id of THREE) pray(g.actor(id), false);
  await g.wait(360);
  // The low morning sun. If it is Mom who has the coin, she knows of another one that was rising and not setting.
  if (me === "mom") await g.say("nevada.flash.sun");
  await g.say(`nevada.flash.${me}`);
  // The coin goes up into the sun, and flashes: once, onto the place that hums.
  const coin = hand(g), arm = g.reach();
  await g.wait(230);                                              // (her arm is out)
  aim(g, coin, PLACE[0], PLACE[1]);
  shine(g, { spark: 1, ray: 0.5, glint: 1 }, coin);
  await g.wait(170);                                              // (and held there)
  await g.tween(230, (k) => shine(g, { spark: 1 - k, ray: 0.5 * (1 - k), glint: 1 }));      // her arm comes down; the light stays where it fell
  await arm;
  // A coin's worth of light: a coin's worth of door.
  g.sfx("portal");
  await g.tween(900, (k) => { put(g, { coin: k, wide: 0 }); shine(g, { glint: 1 - k }); }, g.ease.out);
  // The two tall ones take a step back. Little Sister has started before anybody can say no: it is the height of her eye.
  await Promise.all([g.walkTo(EYE[0], EYE[1], "lilsis"), ...["mom", "bigsis"].map((id) => g.walkTo(BACK[id][0], BACK[id][1], id))]);
  const lil = g.actor("lilsis");
  for (const id of THREE) { const a = g.actor(id); if (a) a.face("E"); }
  // What comes through it. Chickens first: Little Sister hears them before anybody smells a sausage, and her mother confirms her.
  await g.say("nevada.door.1", "nevada.door.2", "nevada.door.2b", "nevada.door.3", "nevada.door.4", "nevada.door.5", "nevada.door.6");
  // Both years. At the first of them, the Roman one, Little Sister asks what B.C. is, with her eye still at the door,
  // and her mother tells her: "before". The second is on Big Sister's timeline, the year Abram went down into Egypt, and
  // her mother knows the chapter. Then Big Sister sees that both are years that matter, and does not know why. A few
  // lines later Little Sister has done the sum her own way.
  await g.say("nevada.gate.2", "nevada.gate.2c", "nevada.gate.2d", "nevada.gate.2b", "nevada.gate.2e", "nevada.gate.2f", "nevada.gate.3");
  if (lil) lil.face("W");                                         // she turns round to them: she told them
  // The top of the scene is hers, word for word. Then Big Sister needs to sit down, Mom has the psalm, and the last two lines are as they were.
  await g.say("nevada.gate.4", "nevada.gate.5", "nevada.gate.5b", "nevada.gate.6", "nevada.gate.7");
  // NEVADA-12SA: it is no longer the end of the demo. The door is open, the size of the coin (#9: nevada.doorOpen), and
  // instead of the title there is one more beat, and then play.
  g.flag("nevada.doorOpen", true);
  await headInTheHole(g);
}

/** After "Some when": her head in the hole (she has to try), Mom lifting her out as one lifts a cat out of a drawer,
    and Big Sister's rule, which is the setup of #12. Little Sister's word about the banjo is said only if she has seen
    it flash (she asked him to play: nevada.banjoFlash). */
async function headInTheHole(g) {
  const lil = g.actor("lilsis"), mom = g.actor("mom"), big = g.actor("bigsis");
  await g.wait(350);
  if (lil) lil.face("E");                                         // back to the door
  await g.say("nevada.hole.1");
  if (lil) {
    await g.moveTo(HEAD[0], HEAD[1], "lilsis");                   // up under it, her face at it
    lil.face("N");
    lil.hold(true);                                               // leaning in, to the ears
  }
  await g.wait(450);
  await g.say("nevada.hole.2");                                   // (muffled)
  if (mom) await g.walkTo(LIFT.mom[0], LIFT.mom[1], "mom");
  if (mom) { mom.face("E"); await mom.play(g.clock, "reach"); }  // she lifts her out, by the collar
  if (lil) { lil.hold(false); await g.moveTo(LIFT.lilsis[0], LIFT.lilsis[1], "lilsis"); lil.face("W"); }
  await g.say("nevada.hole.3");
  if (big) big.look(PLACE[0], PLACE[1]);                          // she has not stopped looking at the hole
  await g.say("nevada.hole.4", "nevada.hole.5");
  await g.say("nevada.shade.rule.1", "nevada.shade.rule.2", "nevada.shade.rule.3", "nevada.shade.rule.mom");
  if (g.flag("nevada.banjoFlash")) await g.say("nevada.shade.rule.lilsis");
}

// ---------- the letterbox: the Son, through the little door ----------
/** Little Sister pushes her lucky penny into the door, for her brother, and the door winks: it waits in the tunnel for
    the Rome end of it, which is next stage's. letterboxTree's `penny` hook, and the penny posted outside a talk. The engine
    sends only from the one being played (g.send); if it is in somebody else's pockets, it goes from there. */
async function sendPenny(g) {
  const holder = g.holder("penny"), lil = g.actor("lilsis"), d = g.store.data;
  if (!holder) return;
  if (lil) {
    if (far(lil, POST)) await g.walkTo(POST[0], POST[1], "lilsis");
    lil.look(PLACE[0], PLACE[1]);
    await lil.play(g.clock, "reach");
  }
  if (holder === d.active) g.send("penny", { to: "son" });
  else {
    const pockets = d.inventory[holder];
    pockets.splice(pockets.indexOf("penny"), 1);
    d.tunnel.push({ item: "penny", from: holder, to: "son", at: Math.round(d.playMs) });
    g.store.emit();
  }
  g.flag("nevada.pennySent", true);
  const c = g.effects.get("door");                               // the door winks
  if (c) {
    await g.tween(200, (k) => c.open(1, { scale: 1 - 0.45 * k }));
    await g.tween(260, (k) => c.open(1, { scale: 0.55 + 0.45 * k }));
  }
  // and she steps back from it, out from in front of it (where she stood, she covered it)
  // (LETTER-17: back to her mother's side, if her mother is on her knees at the door: the first talk)
  const back = kneels(g) ? SIDE.lilsis : LIFT.lilsis;
  if (lil && far(lil, back)) await g.walkTo(back[0], back[1], "lilsis");
  if (lil && kneels(g)) lil.face("E");
}

// ---------- LETTER-17 (round seventeen): the night Mom hears her son ----------
// The letterbox, rewritten as the author asked (16 October; the design is briefs/out/office-hq-design.md, section 2; the
// brief briefs/LETTER-17.md). The moment his voice comes through the little door, Mom's handbag goes down on the gravel
// and she is at the door on her knees (figure.kneel: js/art/rig.js kneelPose, kept to her), facing it, her face at the
// height of it; whoever was speaking into it makes room. When she understands where he is she sits back on her heels,
// and the girls come and stand either side of her; she leans in again to ask if he has eaten. At the end of the first
// talk she gets up, and Grandpa Joe, from his rocker, has a word with her; Ranger brings her the handbag. The handbag on
// the gravel is the rig's own drawing (js/art/props.js `handbag`, a thing on the stage), and the fact nevada.bagDown says
// it is there, so that a game saved in the middle of the talk comes back with it there (setup).
const KNEEL = [600, 578];                       // Mom on her knees at the little door, facing it (E): her face at its height, to its left
const SIDE = { bigsis: [560, 564], lilsis: [624, 589] };     // the girls, either side of her: Big Sister behind her shoulder, Little Sister by the door
const BAG = [578, 592];                         // her handbag, on the gravel beside her
const FETCH = [558, 592];                       // Ranger, beside the handbag, to pick it up (facing E)
const RANGER_PAWS = [23, -26];                  // where his hands are in his reach frames (ranger-reach-1.png: from his foot point, at full size, facing E)
/** Is Mom on her knees at the little door (the first talk)? */
const kneels = (g) => { const m = g.actor("mom"); return !!(m && m.kneeling); };
/** Her handbag: down on the gravel at BAG (true), or on her arm (false); the figure is drawn without it while it is down. */
function bagDown(g, down) {
  const mom = g.actor("mom"), cast = g.view && g.view.cast;
  if (mom) mom.bare = down ? "bag" : null;
  if (!cast) return null;
  if (cast.get && cast.get("handbag")) cast.remove("handbag");
  if (!down || !cast.addThing) return null;
  return cast.addThing("handbag", "handbag", BAG[0], BAG[1], sizeAt(BAG[1]));
}
/** Where the handbag hangs from Ranger's hands, held up (his reach frames): its own foot point, under the strap. */
function inPaws(r) {
  const k = Math.min(1.25, r.scale), side = r.side || 1;
  return [r.x + RANGER_PAWS[0] * k * side, r.y + RANGER_PAWS[1] * k + 15 * sizeAt(r.y)];
}
/** letterboxTree's `kneel`: his voice. Whoever was speaking into the door, and anyone in Mom's way, makes room; Mom comes
    to the door (in a hurry: no other script hurries her); her handbag goes down on the gravel without her looking, and she
    is on her knees, facing the door. Started at his first line; the tree waits for it after the two of them say hello. */
async function momDown(g) {
  const mom = g.actor("mom");
  const inWay = (id) => { const a = g.actor(id); return a && (id === who(g) || Math.hypot(a.x - KNEEL[0], (a.y - KNEEL[1]) * 2.2) < 46 || Math.hypot(a.x - BAG[0], (a.y - BAG[1]) * 2.2) < 30); };
  const room = ["bigsis", "lilsis"].filter(inWay).map((id) => g.walkTo(ASIDE[id][0], ASIDE[id][1], id).then(() => turn(g, id, "E")));
  if (mom) {
    if (Math.hypot(mom.x - KNEEL[0], mom.y - KNEEL[1]) < 12) await g.moveTo(KNEEL[0], KNEEL[1], "mom");
    else { await g.wait(260); mom.hurry = true; await g.walkTo(KNEEL[0], KNEEL[1], "mom"); }
    mom.face("E");
    mom.kneel(true);
    await g.wait(190);                                            // (halfway down: the handbag is on the gravel)
    bagDown(g, true);
    g.flag("nevada.bagDown", true);
    await g.wait(230);
  }
  await Promise.all(room);
}
/** letterboxTree's `heels`: she understands where he is. She sits back on her heels, and the girls come and stand either
    side of her, facing the door. */
async function heels(g) {
  const mom = g.actor("mom");
  if (mom) mom.kneel("back");
  await g.wait(420);
  await Promise.all(["bigsis", "lilsis"].map((id) => (far(g.actor(id), SIDE[id]) ? g.walkTo(SIDE[id][0], SIDE[id][1], id) : null)));
  for (const id of ["bigsis", "lilsis"]) turn(g, id, "E");
  await g.wait(260);
}
/** letterboxTree's `lean`: she leans in to the door again, up on her knees. */
async function lean(g) {
  const mom = g.actor("mom");
  if (mom) { mom.face("E"); mom.kneel(true); }
  await g.wait(400);
}
/** letterboxTree's `rise`: the end of his warning. She gets up off her knees. */
async function momUp(g) {
  const mom = g.actor("mom");
  await g.wait(300);
  if (mom) mom.kneel(false);
  await g.wait(520);
}
/** letterboxTree's `turn`: "Ma'am." She turns to Grandpa Joe, in his rocker; he looks at her, and so does Ranger. */
async function turnToJoe(g) {
  const mom = g.actor("mom"), joe = joeOf(g), r = g.actor("ranger");
  if (mom) mom.face("W");
  if (joe) joe.face("E");
  if (r && mom) r.look(mom.x, mom.y);
  await g.wait(350);
}
/** letterboxTree's `bring`: Ranger comes from beside the rocker to the handbag on the gravel, at a scamper, sits up, picks
    it up by its strap, and holds it up to her. */
async function bringBag(g) {
  const r = g.actor("ranger"), bag = g.view && g.view.cast && g.view.cast.get ? g.view.cast.get("handbag") : null;
  if (!r) return;
  await r.sit(false);
  r.hurry = true;
  await g.walkTo(FETCH[0], FETCH[1], "ranger");
  r.face("E");
  r.hold(true);                                                   // up on his haunches, both hands out
  if (bag) {
    const [x0, y0] = [bag.x, bag.y], [x1, y1] = inPaws(r);
    bag.base = r.y + 1;                                           // (in front of him, in his hands)
    await g.tween(220, (k) => bag.place(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k), g.ease.out);
  }
  await g.wait(200);
}
/** letterboxTree's `take`: she bends to him and takes it, and the handbag is on her arm again. He sits back. */
async function takeBag(g) {
  const mom = g.actor("mom"), r = g.actor("ranger"), cast = g.view && g.view.cast, bag = cast && cast.get ? cast.get("handbag") : null;
  if (mom && r) mom.look(r.x, r.y);
  const bend = mom ? mom.play(g.clock, "pick") : Promise.resolve();
  await g.wait(200);
  if (bag && mom) {
    const [x0, y0] = [bag.x, bag.y], x1 = mom.x + (r && r.x < mom.x ? -10 : 10) * mom.scale, y1 = mom.y - 52 * mom.scale;
    await g.tween(160, (k) => bag.place(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k), g.ease.out);
  }
  bagDown(g, false);
  g.flag("nevada.bagDown", false);
  if (r) r.hold(false);
  await bend;
  if (mom) mom.face("W");
}
/** After the first talk: Ranger goes back to his place beside the rocker and sits up, and Grandpa Joe looks down the road
    again; Mom turns back to the door. */
async function afterLetterbox(g) {
  const r = g.actor("ranger"), joe = joeOf(g), mom = g.actor("mom");
  if (mom) mom.face("E");
  if (joe) joe.face("SE");
  if (r) {
    r.hurry = false;
    await g.walkTo(RANGER[0], RANGER[1], "ranger");
    await g.moveTo(RANGER[0], RANGER[1], "ranger");               // (the walk ends at the edge of the chair's patch of ground: the last step onto his place)
    await r.sit(true);
    r.face("SE");
  }
}
const LETTERBOX = letterboxTree({ penny: sendPenny, kneel: momDown, heels, lean, rise: momUp, turn: turnToJoe, bring: bringBag, take: takeBag });
/** NEVADA-12SA: after anything done at the little door. Whoever goes to it stands at DOORSIDE, to its left; if one of the
    others is standing there already, the engine puts her beside her, which is right in front of the door, and there she
    would hide it from everyone else afterwards (the three of them can be clicked, and they lie over what is behind them).
    So whoever ends up in front of it steps back to the side when she is done. */
async function stepOff(g) {
  const me = g.lead;
  if (me && me.x > 606 && me.x < 686 && me.y > 540 && ASIDE[me.id]) await g.walkTo(ASIDE[me.id][0], ASIDE[me.id][1]);
}
/** A line said at the little door, and then a step to the side if she is in front of it. */
const atDoor = (line) => async (g) => { await g.say(typeof line === "string" ? line : line[who(g)]); await stepOff(g); };
/** The little door, spoken into (after #9): a talk with the Son, held through the door. His words are his portrait's.
    (LETTER-17: a first talk broken off, by a game saved in the middle of it, is picked up with Mom at the door on her
    knees again; and after the first talk, Ranger goes back to his place.) */
async function talkThrough(g) {
  const first = !g.flag("nevada.heardSon");
  if (g.lead) g.lead.look(PLACE[0], PLACE[1]);
  if (first && g.flag("nevada.sonMet") && !kneels(g)) await momDown(g);
  await g.talk(LETTERBOX, { through: "son" });
  if (first && g.flag("nevada.heardSon")) await afterLetterbox(g);
  await stepOff(g);
}
/** Her penny, posted into the little door outside a talk. */
async function postPenny(g) {
  if (g.flag("nevada.pennySent") || !g.holder("penny")) return atDoor(g.fallback("nope"))(g);
  await g.say("nevada.door.penny");
  await sendPenny(g);
  await stepOff(g);
}

// ---------- #12: Mom's car, which never shone ----------
/** Mom's car, looked at once they know they need a bigger shine: the exchange the design wrote for it (once). */
async function car(g) {
  if (g.flag("nevada.doorOpen") && !g.flag("nevada.wideOpen") && !heard(g, "nevada.shade.car.lilsis.2"))
    return g.say("nevada.shade.car.mom.1", "nevada.shade.car.bigsis", "nevada.shade.car.lilsis.1", "nevada.shade.car.mom.2", "nevada.shade.car.lilsis.2");
  return g.say(`nevada.car.look.${who(g)}`);
}

// ---------- #13, the gate: going out and coming in ----------
/** Grandma Jolene, by the hat of the visit (the store counts its visits; the rule is SCENES-12's). */
const hatOf = (g) => ((Math.max(1, Number(g.flag("nevada.visits")) || 1) - 1) % 5) + 1;
const joleneKind = (g) => (hatOf(g) === 1 ? "jolene" : "jolene-" + hatOf(g));
/** Jolene comes out of the shop's door onto the porch (for Big Sister's goodbye), and goes back in. */
async function joleneOut(g) {
  const cast = g.view.cast;
  if (cast.get("jolene")) cast.remove("jolene");
  const j = cast.addFigure("jolene", joleneKind(g), JOLENE_IN[0], JOLENE_IN[1], sizeAt(JOLENE_IN[1])).face("S");
  j.fade(0);
  await g.tween(300, (k) => j.fade(k));
  await g.moveTo(JOLENE_OUT[0], JOLENE_OUT[1], "jolene");
  j.face("SE");
  return j;
}
async function joleneIn(g, j) {
  if (!j) return;
  await g.moveTo(JOLENE_IN[0], JOLENE_IN[1], "jolene");
  await g.tween(300, (k) => j.fade(1 - k));
  g.view.cast.remove("jolene");
}
const turn = (g, id, dir) => { const a = g.actor(id); if (a) a.face(dir); };
/** Into the door: she walks into it and is gone as she reaches it. */
async function into(g, id, delay) {
  const a = g.actor(id);
  if (!a) return;
  await g.wait(delay);
  const walk = g.moveTo(INTO[id][0], INTO[id][1], id);
  await g.wait(240);
  await g.tween(520, (k) => a.fade(1 - k), g.ease.in);
  await walk;
  a.fade(0);
}
/** The wide door, used (#13). Whoever goes first must have the coin ("The coin comes with us"); anyone who is not at
    the door yet is called by Little Sister (an open door must not be kept open). Then the goodbyes, each in her own way
    (Jolene comes out onto the porch for hers), Mom's and Grandpa Joe's (LETTER-17: "Will you be all right? Out here?" ...
    "Porch light on. However long it takes."), the psalm in two halves, "Girls. Hold hands. All the way through.", and they
    go in hand in hand, Little Sister in the middle. Then the cut-scene "Backup" (SCENES-12C). The coin goes with them, the
    egg with Little Sister; the sun shade stays with Grandpa Joe. */
async function goThrough(g) {
  const me = who(g);
  if (!g.flag("nevada.wideOpen")) return g.say(`nevada.through.small.${me}`);
  if (!g.has("coin")) return g.say("nevada.through.coin.mom");
  const late = THREE.filter((id) => { const a = g.actor(id); return a && Math.hypot(a.x - LINE[id][0], (a.y - LINE[id][1]) * 2.2) > 170; });
  if (late.some((id) => id !== "lilsis")) await g.say("nevada.through.rude.lilsis");
  // In front of the door, in a row: Mom, Little Sister, Big Sister.
  await Promise.all(THREE.map((id) => g.walkTo(LINE[id][0], LINE[id][1], id)));
  for (const id of THREE) turn(g, id, "N");
  // Little Sister turns to the porch and says goodbye to everybody, hens and all; Ranger looks at her.
  turn(g, "lilsis", "W");
  const r = g.actor("ranger"), lil = g.actor("lilsis");
  if (r && lil) r.look(lil.x, lil.y);
  await g.say("nevada.through.lilsis.1");
  // Grandma Jolene comes out onto the porch, in the hat of the hour, for Big Sister's.
  turn(g, "bigsis", "W");
  const jolene = await joleneOut(g);
  await g.say("nevada.through.bigsis.1", "nevada.through.jolene.1", "nevada.through.bigsis.2");
  await joleneIn(g, jolene);
  // Mom, to Grandpa Joe, with her hand out; the two of them (LETTER-17: the promise, "Porch light on."); and the psalm,
  // his half and hers.
  turn(g, "mom", "W");
  turn(g, "bigsis", "N");
  await g.actor("mom")?.play(g.clock, "reach");
  await g.say("nevada.through.mom.1", "nevada.through.mom.4", "nevada.through.joe.5", "nevada.through.mom.5", "nevada.through.joe.6",
    "nevada.through.joe.2", "nevada.through.mom.2", "nevada.through.joe.4");
  for (const id of THREE) turn(g, id, "N");
  await g.say("nevada.through.mom.3");
  // Hand in hand, Little Sister in the middle, into the door.
  g.sfx("portal");
  await Promise.all([into(g, "mom", 0), into(g, "lilsis", 60), into(g, "bigsis", 120)]);
  g.flag("nevada.left", true);
  await g.cutscene("backup");
}

export default {
  id: "nevada-roadside",
  era: "nevada",
  name: "The last stop before nothing",
  travel: (g) => !g.flag("nevada.left"),                   // MAP-15: not by the map once the act has ended (whatever a save catches it in)

  // Every place in this file is the painter's own measurement of the finished picture (art/scenes/nevada-roadside/layout.json),
  // or was set by eye against the picture with the people standing in it; where the two differ the comment says why.

  // DEPTH. Out of doors, on flat ground that runs back to the foot of the mesas.
  horizon: 290, full: 590,

  // The dirt lot: from the car, bottom left, to the fence, and back as far as the shack's porch and the foot of the fence.
  walk: { area: [[0, 470], [40, 464], [104, 458], [150, 450], [262, 444], [270, 461], [410, 461], [414, 448], [540, 444], [600, 441], [640, 446], [760, 452], [800, 455], [800, 498], [738, 506], [722, 560], [652, 588], [600, 596], [0, 596]] },
  // The patch of sand that turned to glass. Nobody walks on it: Mom has said so.
  blocked: [[[580, 534], [600, 522], [640, 518], [690, 521], [714, 536], [690, 549], [640, 553], [602, 549]]],

  party: ["mom", "bigsis", "lilsis"],
  // They have just got out of the car, and stand looking at the place. (The painter's marks are a little lower and
  // closer together: 268, 572 for Mom, 318, 588 for Big Sister and 232, 554 for Little Sister. There the car's own
  // patch of ground takes Little Sister's place, and whatever she says is written across her mother's face, because
  // words go over a speaker's head and hers is the lowest. So the little one stands a row behind the other two.)
  // NEVADA-12SA: and the way back out of the store (its `door`: g.goto("nevada-roadside", { spawn: "fromStore" })): the one
  // leading on the porch in front of the shop's door, the other two on the lot just outside it, either side. Big Sister
  // stands a row back now, too, at the right of the three (320, 546): at 334, 576 she hid half of Ranger, who sits at
  // 352, 512, and anywhere in the front row her words were written across Grandpa Joe's face in his rocker while her
  // mother talked to him.
  spawn: { default: [286, 562], mom: [286, 562], bigsis: [320, 546], lilsis: [248, 528], fromStore: [261, 452] },
  arrive: { fromStore: [[218, 462], [306, 474]] },
  facing: "E",
  exits: ["nevada-store"],                                        // NEVADA-12SA: (its pictures are made ready while they are out here)
  // No `edges` (round three: a way out across the edge of the picture). This scene has no way out but the shop's door:
  // the car brought them, and the only way on is the door in time where the tracks stop.

  picture: art + "back.png",
  planes: [
    { id: "pump", src: art + "pump.png", base: 452 },
    { id: "stand", src: art + "stand.png", base: 493, solid: [[410, 474], [546, 474], [548, 497], [408, 497]] },                  // the lemonade stand, and the ground under its table
    // Mom's car has come in from the left, and its tail is still off the edge of the picture.
    { id: "car", src: art + "car.png", base: [[0, 592], [225, 539]], solid: [[0, 535], [231, 535], [199, 596], [0, 596]] },
    { id: "front", src: art + "front.png", plane: "front" },      // the rusty drum and the sagebrush at the bottom right corner
    // Two that are not pictures: the patch of ground the man in gray is standing on. He moves when the story does, and
    // a cut-out's `solid` follows the story where a person's own does not.
    { id: "agent-ground", solid: [[641, 448], [681, 448], [681, 464], [641, 464]], when: (g) => !g.flag("nevada.distracted") && !g.flag("nevada.backup") },
    { id: "agent2-ground", solid: [[732, 458], [772, 458], [772, 474], [732, 474]], when: (g) => !!g.flag("nevada.distracted") && !g.flag("nevada.backup") },
    // NEVADA-12SA: the sun shade from the store's window, in Grandpa Joe's hands (PAINT-12A: shade-held.png, an alt), from
    // #12 until the cut-scene takes it down. Its base is a row below his feet, so it lies over him and his fists show round it.
    { id: "shade-held", src: art + "shade-held.png", base: 561, when: holding },
    // NEVADA-12SA: and while the wide door is open, nobody stands right in front of it (who stood there would be behind it).
    { id: "door-ground", solid: [[600, 552], [700, 552], [700, 565], [600, 565]], when: (g) => holding(g) && !gone(g) },
  ],

  // LIGHT, drawn live. All of it starts out of sight: `setup` and the scripts bring it on.
  //   #ray     the faint beam from what flashes to the spot
  //   #glint   the spot of reflected sunlight, on the place
  //   #spark   the flash of the coin itself, in her hand (she is drawn over it: what shows is what sticks out round her fist)
  //   #burst   the chrome of Grandpa Joe's banjo catching the low sun (he is drawn over it: a burst of light round the banjo)
  //   #sheen   the sun shade's flash, a windshield's worth (the shade is drawn over it: a halo round the panel)
  //   (The door in time is not drawn here: it is the paint itself, bending, with a wet rim and a bright heart so that it
  //   shows on the sand in broad daylight. See `fx`.)
  live() {
    return `<defs>
        <radialGradient id="glint-glow"><stop offset="0" stop-color="#ffffff" stop-opacity="1"/><stop offset="0.4" stop-color="#fff3c2" stop-opacity="0.75"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>
        <radialGradient id="sheen-glow"><stop offset="0.45" stop-color="#ffffff" stop-opacity="0.95"/><stop offset="0.7" stop-color="#fff6d2" stop-opacity="0.55"/><stop offset="1" stop-color="#ffefb8" stop-opacity="0"/></radialGradient>
      </defs>
      <ellipse id="sheen" cx="658" cy="445" rx="104" ry="70" fill="url(#sheen-glow)" opacity="0"/>
      <polygon id="ray" points="0,0 0,0 0,0" fill="#fffbe6" opacity="0" shape-rendering="geometricPrecision"/>
      <g id="glint" opacity="0" shape-rendering="geometricPrecision"><circle r="15" fill="url(#glint-glow)"/><ellipse rx="4" ry="5" fill="#ffffff"/></g>
      <g id="spark" opacity="0" shape-rendering="geometricPrecision"><circle r="12" fill="url(#glint-glow)"/><path d="M-16,0 L16,0 M0,-16 L0,16" stroke="#ffffff" stroke-width="1.6" stroke-linecap="round"/></g>
      <g id="burst" opacity="0" shape-rendering="geometricPrecision"><circle r="30" fill="url(#glint-glow)"/><path d="M-38,0 L38,0 M0,-38 L0,38 M-17,-17 L17,17 M-17,17 L17,-17" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round"/></g>`;
  },

  // THINGS THAT MOVE BY NATURE (round four: briefs/out/paint-4b-ready.md): the two big birds that were painted still in
  // the sky cross it slowly now and then, and Grandpa Joe has his coffee on: a thread of woodsmoke from the stovepipe,
  // nearly straight up in the still morning (the wind sock hangs slack: there is no wind).
  fx: [
    // The door in time (round ten): a ripple in the paint, the size of a coin, in the air over the glass where the tracks
    // stop; at its depth, the three of them at the glass are drawn in front of it, and the man along the fence behind.
    { id: "door", type: "portal", at: PLACE, r: 10, base: PLACE[1] + 1, pale: "#fffaf0", strength: 0.8 },      // (a coin door bends harder than the walk-in door, or it is not seen on the sand: the study's advice)
    // NEVADA-12SA: the door at its other two sizes (see SIZES, above): the banjo's, round, and the windshield's, a doorway.
    // It is drawn over the shade in Grandpa Joe's hands, and bends it with the sand (`under`): it is light, and a door the
    // height of a woman that the shade hid the top of would not read as one (PAINT-12A's note 3). Its reach keeps clear of
    // him, at the corner of the glass. Whoever stands behind its foot is behind it: that is how they go in (#13). It bends
    // as hard as a door can (strength 1, and most of it into the bending): a door this big has no bright heart and no wet
    // rim (those are for a coin-sized one), and at the walk-in door's own strength its rings were lost on the sand.
    { id: "wide", type: "portal", at: PLACE, r: 66, wide: 0.45, base: 562, under: ["shade-held"], pale: "#fffaf0", strength: 1, bend: 0.9 },
    { id: "birds", type: "birds", kind: "flyers", lanes: [[[-20, 168], [820, 128]], [[820, 54], [-20, 92]], [[-20, 112], [820, 70]]], every: [25, 55], group: [1, 2], speed: 34, color: "#2e3a5c", size: [7, 10],
      frames: { glide: "bird-0.png", flap: ["bird-1.png", "bird-0.png", "bird-2.png", "bird-0.png"], bank: "bird-3.png", middle: [7, 5.5] } },
    { id: "stovepipe", type: "smoke", at: [305.2, 279.7], base: 419, color: "#e6e2ea", opacity: 0.3, height: 46, width: [1.5, 7], lean: [4, -46], rate: 2 },
  ],

  // THEIR OWN LIVES (round four: js/engine/life.js).
  actors: [
    // NEVADA-12SA: Grandpa Joe, in his rocking chair (drawn with him), where the old-timer's lawn chair was, with the banjo
    // across his knees. Now and then he gets up out of it, slowly (the chair stays put), and takes a few steps: back toward
    // his pump and his shack, rubbing the small of his back, or out in front to look down the road; and sits down again.
    // Sitting, his own small movements are a strum, a slow rock and a touch to his hat (people.js). From #12 he is on his
    // feet at the glass, holding the sun shade (`setup` puts him there): his life waits. After the cut-scene he is gone.
    { id: "grandpajoe", kind: "grandpajoe", at: JOE, face: "SE", when: (g) => !g.flag("nevada.backup"),
      life: { every: [26, 48], spots: [[338, 468, "NE"], [372, 536, "SE"]], stay: [4, 8], when: (g) => !holding(g) } },
    // NEVADA-12SA: Ranger, sitting up on the ground beside the chair, on our side of it (painted frames: ranger.json). Now
    // and then he goes over to the lemonade stand and washes a pebble in front of it, and comes back. In the mirror shades
    // from the trade on (`setup`: his frames' `shades` set).
    { id: "ranger", kind: "ranger", at: RANGER, face: "SE", sit: true, when: (g) => !g.flag("nevada.backup"),
      life: { every: [22, 44], spots: [[424, 506, "N"]], stay: [4, 9] } },
    // The man in gray: in front of the notice, and then a few yards along the fence. (The ground he stands on is among the cut-outs, above.)
    // While he is in front of the notice he keeps it covered (the story needs him there): small movements only, his
    // watch and his tie. Once he has stepped aside he paces a little along the fence, never back in front of it.
    { id: "agent", kind: "agent", at: [661, 458], face: "S", solid: false, when: (g) => !g.flag("nevada.distracted") && !g.flag("nevada.backup"),
      life: { still: true, fidget: [5, 11] } },
    { id: "agent", kind: "agent", at: [752, 468], face: "E", solid: false, when: (g) => !!g.flag("nevada.distracted") && !g.flag("nevada.backup"),
      life: { every: [18, 34], spots: [[726, 480, "W"], [784, 482, "E"]], stay: [2.5, 5] } },
  ],

  // Make the picture match the story facts. Runs on arrival and after loading a save.
  setup(g) {
    shine(g);
    put(g, SIZES[holding(g) ? "wide" : g.flag("nevada.doorOpen") ? "coin" : "shut"]);
    banjoNow = null;
    const r = g.actor("ranger");
    if (r) r.variant(g.flag("nevada.traded") ? "shades" : null);
    // From #12 until the cut-scene, Grandpa Joe stands at the glass holding the sun shade, and the rocker is empty.
    const joe = joeOf(g);
    if (holding(g) && joe && joe.kind === "grandpajoe") { joe.sit(false, true); swapJoe(g, "grandpajoe-shade", HOLD, "E"); }
    // Once they have gone through (a game saved before the cut-scene has played), none of the three is on the stage.
    if (gone(g)) for (const id of THREE) { const a = g.actor(id); if (a) a.fade(0); }
    // LETTER-17: Mom's handbag, down on the gravel while the fact says so (a game saved in the middle of the first talk
    // through the little door: she comes back to it, and kneels, when the talk is picked up again)
    bagDown(g, !!g.flag("nevada.bagDown"));
  },

  /** NEVADA-12SA: the door in time, to a size, for whoever needs it (SCENES-12): g.scene.door(g, "shut" | "coin" | "banjo" | "wide", ms). */
  door(g, size, ms = 0) { return sizeDoor(g, size, ms); },

  // Back to front: a later area lies over an earlier one.
  // SHAPES (round three: the Show button outlines each thing, so each shape hugs its thing, a few pixels outside its edge).
  // They were traced from the painter's picture and cut-outs, and the people from the figures the engine draws at their
  // marks (round twelve: Grandpa Joe in his rocker, Ranger, and Grandpa Joe holding the shade). A thing that is a painted
  // cut-out names it (`plane`): Show then outlines the cut-out's own edge. The notice was already tight. The three of the
  // family are clickable too (the engine puts an area over each one standing here), so no shape lies over the places where
  // they stand: where they arrive, and where they are sent to stand (the places to stand below, and the places above).
  hotspots: [
    { id: "shack", name: "shack", poly: [[128, 331], [166, 312], [166, 277], [203, 277], [204, 262], [211, 240], [220, 242], [216, 263], [216, 277], [279, 277], [279, 300], [299, 299], [300, 273], [311, 273], [311, 300], [348, 298], [348, 412], [327, 420], [326, 425], [312, 426], [262, 426], [132, 426], [128, 422]], walkTo: [254, 449], face: "N", look: each("nevada.shack") },      // its sign, its wind arrow and its stovepipe; down to its porch, and no lower (Mom's head is just under it when they arrive)
    // NEVADA-12SA: the shop's door on the porch: the way into the store (the three go in together), and the spare hat on
    // the nail in the porch post beside it (the painter's `store` and `hat-nail`; they lie over the shack).
    { id: "store", name: "store", verb: "Go into", poly: [[245, 415], [281, 417], [281, 337], [245, 337]], walkTo: STORE, face: "N", look: each("nevada.porch.door"),
      use: (g) => g.goto("nevada-store", { spawn: "fromLot" }) },
    { id: "hat-nail", name: "hat on the nail", rect: [277, 356, 25, 15], walkTo: [291, 466], face: "N", look: each("nevada.hatnail") },
    { id: "fence", name: "fence", poly: [[562, 291], [614, 319], [800, 309], [800, 333], [617, 333], [617, 434], [606, 434], [603, 412], [562, 298]], walkTo: [590, 456], face: "N", look: each("nevada.fence") },      // its far side, its corner post, and the barbed wire along the top of its near side (the notice and the men are kept out of it)
    { id: "notice", name: "notice", verb: "Read", poly: [[630, 402], [695, 405], [695, 361], [630, 359]], walkTo: [646, 472], face: "N", look: readNotice, use: readNotice },
    { id: "pump", name: "gas pump", plane: "pump", poly: [[346, 348], [340, 352], [338, 357], [339, 364], [344, 370], [340, 372], [336, 378], [336, 433], [334, 442], [362, 443], [365, 439], [363, 428], [370, 426], [372, 422], [372, 392], [368, 385], [363, 384], [362, 374], [355, 370], [361, 361], [359, 352], [353, 348]], walkTo: [346, 466], face: "N", look: each("nevada.pump") },
    { id: "stand", name: "lemonade stand", plane: "stand", poly: [[490, 316], [486, 318], [485, 325], [413, 344], [416, 352], [428, 357], [437, 356], [448, 362], [463, 362], [478, 369], [474, 387], [474, 431], [471, 432], [467, 428], [452, 428], [444, 432], [443, 419], [431, 418], [424, 426], [423, 432], [415, 433], [416, 445], [420, 447], [420, 451], [428, 454], [423, 477], [426, 483], [425, 494], [428, 496], [431, 494], [435, 475], [439, 476], [439, 483], [449, 496], [453, 490], [472, 490], [475, 483], [480, 483], [486, 491], [503, 491], [507, 496], [512, 490], [513, 483], [522, 482], [525, 494], [531, 494], [522, 447], [537, 446], [539, 441], [530, 426], [524, 427], [520, 432], [516, 429], [490, 432], [480, 425], [483, 370], [485, 367], [491, 367], [501, 372], [518, 372], [526, 376], [539, 374], [544, 377], [551, 375], [553, 367], [492, 326], [493, 318]], walkTo: [486, 522], face: "N", look: each("nevada.stand") },      // its umbrella, its table and its sign
    {
      // NEVADA-12SA: Grandpa Joe in his rocker (him, the chair and the banjo, as the game draws them). Talked to: his tree.
      id: "grandpajoe", name: "Grandpa Joe", verb: "Talk to", poly: [[384, 406], [384, 409], [359, 414], [367, 480], [349, 482], [348, 485], [360, 494], [356, 496], [357, 499], [395, 502], [395, 506], [409, 506], [409, 503], [425, 501], [425, 498], [421, 496], [419, 469], [410, 464], [411, 457], [414, 455], [411, 451], [440, 435], [440, 433], [439, 431], [394, 430], [393, 419], [400, 417], [400, 415], [393, 414], [391, 406]],
      walkTo: [432, 528], face: "NW", when: (g) => !holding(g) && !g.flag("nevada.backup"),
      look: each("nevada.old.look"), use: talkToJoe, useWith: { coin: "nevada.old.coin", storeshade: shadeToJoe },
    },
    {
      // NEVADA-12SA: Ranger, sitting up beside the chair (his frames, as the game draws them). Talked to: his tree; the
      // mirror shades, held out to him: the trade (#10); a penny: he sniffs it and hands it back.
      id: "ranger", name: "Ranger", verb: "Talk to", poly: [[349, 472], [340, 504], [336, 507], [337, 514], [366, 514], [369, 504], [363, 501], [365, 496], [361, 490], [367, 488], [369, 484], [362, 478], [361, 472]],
      walkTo: [298, 520], face: "E", when: (g) => !g.flag("nevada.backup"),
      look: (g) => g.say(`nevada.ranger.${g.flag("nevada.traded") ? "look2" : "look"}.${who(g)}`), use: talkToRanger,
      useWith: { mirrorshades: shadesToRanger, penny: pennyToRanger, pennies: pennyToRanger, coin: "nevada.old.coin" },
    },
    // The man in gray, before and after he backs off along the fence: Show outlines his own figure (the person "agent"), inside the area.
    {
      id: "agent", name: "man in gray", verb: "Talk to", poly: [[659, 365], [654, 368], [652, 373], [655, 379], [646, 384], [643, 398], [649, 403], [648, 458], [653, 462], [661, 455], [668, 462], [673, 458], [672, 403], [678, 398], [675, 384], [666, 379], [669, 376], [667, 368]], walkTo: [626, 476], face: "NE", when: (g) => !g.flag("nevada.distracted") && !g.flag("nevada.backup"),
      look: each("nevada.agent.look"), use: talkToAgent, useWith: { coin: ["nevada.agent.coin.1", "nevada.agent.coin.2"] },
    },
    {
      id: "agent2", name: "man in gray", verb: "Talk to", plane: "agent", actor: "agent", poly: [[750, 371], [744, 377], [746, 388], [736, 400], [736, 412], [745, 430], [746, 470], [757, 472], [761, 469], [761, 463], [757, 460], [757, 447], [763, 402], [760, 388], [763, 381], [759, 373]], walkTo: [708, 482], face: "E", when: (g) => !!g.flag("nevada.distracted") && !g.flag("nevada.backup"),
      look: each("nevada.agent.look"), use: talkToAgent, useWith: { coin: ["nevada.agent.coin.1", "nevada.agent.coin.2"] },
    },
    // Mom's car. (NEVADA-12SA: once they know that a bigger shine is wanted, a look at it is #12's first wrong try: it never shone.)
    { id: "car", name: "Mom's car", plane: "car", verb: "Look at", poly: [[0, 423], [0, 582], [112, 582], [121, 586], [132, 586], [141, 582], [156, 582], [159, 580], [162, 569], [180, 569], [187, 564], [218, 523], [223, 520], [226, 505], [224, 486], [219, 475], [206, 466], [186, 460], [158, 457], [100, 425], [81, 421], [22, 421]], walkTo: [229, 588], face: "W", look: car, use: car },
    {
      // The glass where the tracks stop, and the last stretch of the two ruts that run into it. The place that hums is in
      // the air over it (once it is open, the door there has an area of its own, below). (The ruts higher up are left out:
      // the family stand on them and between them, to read the notice, to talk to the man in gray, and beside him once he has moved.)
      id: "tracks", name: "where the tracks stop", verb: "Go to", poly: [[595, 492], [613, 492], [604, 518], [694, 522], [693, 492], [709, 492], [711, 522], [726, 526], [738, 532], [740, 540], [733, 548], [700, 553], [650, 557], [620, 557], [590, 551], [572, 546], [560, 538], [558, 530], [566, 523], [585, 518]], walkTo: [548, 548], face: "E",
      // (Her flashlight, tried here: light is the right idea, and this is too little of it. Whoever holds it, she is the one who says so.)
      look: each("nevada.tracks.look"), use: atTheTracks,
      useWith: { coin: coinAtTheTracks, lilflash: "nevada.tracks.lilflash", storeshade: shadeToGlass, penny: (g) => (g.flag("nevada.doorOpen") && !g.flag("nevada.wideOpen") ? postPenny(g) : g.say(g.fallback("nope"))) },
    },
    {
      // NEVADA-12SA: Grandpa Joe at the corner of the glass, holding the sun shade to the sun (him, as the game draws him
      // there; the panel itself, over the place, is the door's). He can still be talked to: he talks with his head.
      id: "joe-holding", name: "Grandpa Joe", verb: "Talk to", actor: "grandpajoe", poly: [[564, 413], [563, 421], [554, 423], [554, 425], [562, 427], [564, 436], [564, 443], [559, 450], [558, 473], [555, 474], [555, 486], [559, 487], [562, 495], [564, 544], [563, 553], [544, 557], [544, 561], [550, 563], [550, 566], [593, 566], [593, 563], [599, 561], [597, 556], [578, 551], [580, 507], [584, 487], [603, 484], [602, 476], [589, 474], [587, 462], [601, 459], [608, 437], [603, 432], [587, 431], [584, 427], [594, 425], [594, 423], [584, 421], [583, 413]],
      walkTo: [520, 584], face: "E", when: holding,
      look: each("nevada.joe.holding"), use: talkToJoe, useWith: { coin: "nevada.old.coin" },
    },
    {
      // NEVADA-12SA: the little door, open (after #9), the size of the coin, in the air over the glass: spoken into, it is
      // the letterbox (the Son, on the other side of it, in Rome); her penny goes in, for luck.
      id: "hole", name: "little door", verb: "Talk into", circle: [PLACE[0], PLACE[1], 16], walkTo: DOORSIDE, face: "NE",
      when: (g) => !!g.flag("nevada.doorOpen") && !g.flag("nevada.wideOpen"),
      look: atDoor(each("nevada.through.small")), use: talkThrough,
      useWith: { penny: postPenny, pennies: atDoor("nevada.pennies.keep"), egg: atDoor("nevada.egg.keep"), coin: atDoor("nevada.gate.6") },
    },
    {
      // NEVADA-12SA: the door, wide open in Grandpa Joe's light (#12): gone through, it is the gate (#13).
      id: "door", name: "door", verb: "Go through",
      poly: [[646, 410], [659, 413], [669, 423], [676, 438], [679, 461], [679, 483], [679, 505], [676, 528], [669, 543], [659, 553], [646, 556], [633, 553], [623, 543], [616, 528], [613, 505], [613, 483], [613, 461], [616, 438], [623, 423], [633, 413]],
      walkTo: LINE.lilsis, face: "N", when: (g) => holding(g) && !gone(g),
      look: each("nevada.shade.done"), use: goThrough, useWith: { coin: goThrough },
    },
  ],

  // Handing the coin over. Big Sister is the one who knows what it is. (The things they brought from the house can be
  // handed about too, and this scene has nothing to add: the game's own line is said, and that is all.)
  // NEVADA-12SA: and Little Sister will not part with the warm egg or the three pennies: she says so, and has them back.
  async given(g, item, to, from) {
    if (item === "coin") {
      if (to === "bigsis" && !g.flag("nevada.coinRead")) await readCoin(g);
      else if (to === "lilsis") await g.say("nevada.coin.lilsis");
      else if (to === "mom") await g.say("nevada.coin.mom");
      return;
    }
    if ((item === "egg" || item === "pennies") && from === "lilsis") {
      await g.say(item === "egg" ? "nevada.egg.keep" : "nevada.pennies.keep");
      const d = g.store.data, theirs = d.inventory[to] || [], i = theirs.indexOf(item);
      if (i >= 0) { theirs.splice(i, 1); d.inventory.lilsis.push(item); g.store.emit(); }
    }
  },

  talk: {
    mom: {
      bigsis: [
        { when: (g) => g.has("coin") && !g.flag("nevada.coinRead"), say: ["nevada.talk.mom.bigsis.coin.a", "nevada.talk.mom.bigsis.coin.b"] },
        { when: (g) => !!g.flag("nevada.coinRead"), say: ["nevada.talk.mom.bigsis.quarter.a", "nevada.talk.mom.bigsis.quarter.b"] },      // whose face is on the money, and what ours says
        ["nevada.talk.mom.bigsis.1a", "nevada.talk.mom.bigsis.1b"],
        ["nevada.talk.mom.bigsis.2a", "nevada.talk.mom.bigsis.2b", "nevada.talk.mom.bigsis.2c"],
        // NEVADA-12SA: round twelve's, after the old ones (the writer's table: S/work-writer/ids.md)
        { when: (g) => !!g.flag("nevada.traded"), say: ["nevada.talk.mom.bigsis.trade.a", "nevada.talk.mom.bigsis.trade.b"] },
        { when: (g) => (Number(g.flag("nevada.factsTold")) || 0) >= 1, say: ["nevada.talk.mom.bigsis.jolene.a", "nevada.talk.mom.bigsis.jolene.b", "nevada.talk.mom.bigsis.jolene.c"] },
      ],
      lilsis: [
        { when: (g) => !g.flag("nevada.distracted"), say: ["nevada.talk.mom.lilsis.gray.a", "nevada.talk.mom.lilsis.gray.b"] },
        ["nevada.talk.mom.lilsis.1a", "nevada.talk.mom.lilsis.1b"],
        ["nevada.talk.mom.lilsis.2a", "nevada.talk.mom.lilsis.2b"],
        { when: (g) => (Number(g.flag("nevada.visits")) || 0) >= 2, say: ["nevada.talk.mom.lilsis.hats.a", "nevada.talk.mom.lilsis.hats.b"] },      // NEVADA-12SA
        { when: (g) => g.asked("joe/grandpa") > 0, say: ["nevada.talk.mom.lilsis.joe.a", "nevada.talk.mom.lilsis.joe.b"] },                           // NEVADA-12SA
      ],
    },
    bigsis: {
      mom: [
        ["nevada.talk.bigsis.mom.1a", "nevada.talk.bigsis.mom.1b"], ["nevada.talk.bigsis.mom.2a", "nevada.talk.bigsis.mom.2b", "nevada.talk.bigsis.mom.2c"],
        { when: (g) => !!g.flag("nevada.heardSon"), say: ["nevada.talk.bigsis.mom.son.a", "nevada.talk.bigsis.mom.son.b", "nevada.talk.bigsis.mom.son.c"] },      // NEVADA-12SA
      ],
      lilsis: [
        { when: (g) => !g.flag("nevada.distracted"), say: ["nevada.talk.bigsis.lilsis.gray.a", "nevada.talk.bigsis.lilsis.gray.b"] },
        ["nevada.talk.bigsis.lilsis.1a", "nevada.talk.bigsis.lilsis.1b", "nevada.talk.bigsis.lilsis.1c", "nevada.talk.bigsis.lilsis.1d"],
        ["nevada.talk.bigsis.lilsis.2a", "nevada.talk.bigsis.lilsis.2b"],
        { when: (g) => !!g.flag("nevada.jolene"), say: ["nevada.talk.bigsis.lilsis.egg.a", "nevada.talk.bigsis.lilsis.egg.b"] },              // NEVADA-12SA
        { when: (g) => !!g.flag("nevada.banjoTried"), say: ["nevada.talk.bigsis.lilsis.banjo.a", "nevada.talk.bigsis.lilsis.banjo.b"] },     // NEVADA-12SA
      ],
    },
    lilsis: {
      mom: [
        // Once Grandpa Joe has told of Jolene's hens, the next word she has with her mother is about her own chicken.
        { when: (g) => !!g.flag("nevada.hensTold"), say: ["nevada.talk.lilsis.mom.4a", "nevada.talk.lilsis.mom.4b"] },
        ["nevada.talk.lilsis.mom.1a", "nevada.talk.lilsis.mom.1b"], ["nevada.talk.lilsis.mom.2a", "nevada.talk.lilsis.mom.2b", "nevada.talk.lilsis.mom.2c"], ["nevada.talk.lilsis.mom.3a", "nevada.talk.lilsis.mom.3b"],
        { when: (g) => !!g.flag("nevada.jolene"), say: ["nevada.talk.lilsis.mom.egg.a", "nevada.talk.lilsis.mom.egg.b", "nevada.talk.lilsis.mom.egg.c"] },      // NEVADA-12SA
        { when: (g) => !!g.flag("nevada.heardSon"), say: ["nevada.talk.lilsis.mom.son.a", "nevada.talk.lilsis.mom.son.b"] },                                     // NEVADA-12SA
        { when: (g) => !!g.flag("nevada.jolene"), say: ["nevada.talk.lilsis.mom.hens.a", "nevada.talk.lilsis.mom.hens.b", "nevada.talk.lilsis.mom.hens.c"] },   // NEVADA-12SA
      ],
      bigsis: [
        ["nevada.talk.lilsis.bigsis.1a", "nevada.talk.lilsis.bigsis.1b", "nevada.talk.lilsis.bigsis.1c"], ["nevada.talk.lilsis.bigsis.2a", "nevada.talk.lilsis.bigsis.2b", "nevada.talk.lilsis.bigsis.2c"],
        { when: (g) => !!g.flag("nevada.traded"), say: ["nevada.talk.lilsis.bigsis.trade.a", "nevada.talk.lilsis.bigsis.trade.b", "nevada.talk.lilsis.bigsis.trade.c"] },      // NEVADA-12SA
        { when: (g) => (Number(g.flag("nevada.visits")) || 0) >= 2, say: ["nevada.talk.lilsis.bigsis.hats.a", "nevada.talk.lilsis.bigsis.hats.b", "nevada.talk.lilsis.bigsis.hats.c", "nevada.talk.lilsis.bigsis.hats.d"] },      // NEVADA-12SA
      ],
    },
  },

  async enter(g, from) {
    // NEVADA-12SA: a game saved after they went through and before the cut-scene had played: it plays now.
    if (gone(g) && !g.flag("nevada.backup")) return g.cutscene("backup");
    // Out of the store: they come out of its door and look out over the lot.
    if (from === "nevada-store") for (const id of THREE) turn(g, id, "S");
    if (g.flag("nevada.arrived")) return;
    await g.wait(500);
    await g.say("nevada.arrive.1", "nevada.arrive.2", "nevada.arrive.2b", "nevada.arrive.3", "nevada.arrive.4", "nevada.arrive.5");      // (NEVADA-12SA: and "a gentleman on a porch with a banjo")
    g.flag("nevada.arrived", true);
  },
};

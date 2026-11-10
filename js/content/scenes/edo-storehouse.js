// Act Six, the second leg: inside the charcoal-burner's storehouse in the hills north of Osaka (SCENES-20B: new in round
// twenty, replacing ENGINE-20's stub; briefs/SCENES-20.md, and the design, briefs/out/edo-design.md, #25 and #27). A small dim
// room of dark boards, the rain loud on the thatch: charcoal sacks against the walls, tools, baskets, straw rope, a lantern
// on a hook, the front door barred on the inside, the small high window in the back wall with sacks under it, and on the
// floor a straw mat over a trapdoor. Light between the floorboards when the room below is lit.
//
//   #25 Under The Cedars  Little Sister comes in by the window (edo-cedars.js) and lands on the sacks, alone; she lifts the
//                         bar (edo.unbarred) and the others come in. The mat with light at its edge: moved, a trapdoor
//                         (edo.matMoved, and the exchange: "We should not open that." "No. We should knock."); a knock on
//                         it, the light below goes out and comes up again (edo.knocked); and down (edo.hidden: edo-chapel).
//   the night             the lantern lit again (edo.trusted); the room is the way up from below and out to the path.
//   #27 Charcoal, And A Kind Child   the morning: Jinsuke keeps the door, O-Rin by the lantern. The mat back over the
//                         trapdoor and eleven sacks over the mat (Big Sister and O-Rin: edo.sacksHid); the pink light up
//                         between the boards (Little Sister's flashlight, left on below: off, edo.pinkOff, edo-chapel.js);
//                         Mom below (edo.momBelow: edo-hills.js keepBelow). Each thing done, the constable climbs a step
//                         nearer up the path (edo-hills.js afterStep); all three, he knocks, and is let in, asks, and is
//                         answered truly; the egg (talk/edo-b.js isukeTree); he goes; "Come down... the sun is on the ladder."
//   wrong tries           the door before the room is ready (Jinsuke's reason: NOT_READY), Mom up here (Big Sister's "Not up
//                         here, Mother."), Big Sister answering for Mom (the tree's own wrong foot).
//
// Every place is PAINT-20C's own measurement of the finished picture (art/scenes/edo-storehouse/layout.json and its
// ready.md); where a place was set by eye the comment says so.
//
// Try it: index.html?scene=edo-storehouse&lead=lilsis&flags=edo.sailed,edo.boated  (dressed by script as LEG_START.hills has them; SCENES-21B: and edo.boated)

import { STOCK_DRESSED, is } from "./edo-common.js";
import { GIRLS, who, each, heard, morning, sunUp, raining, hats, TALK, keepBelow, passing, partyOf, sceneOf, STORE, ISUKE_WAY, isukeAt,
  afterStep, talkToIsuke, notReady, toPath, inPoly, clearOf, pinkOn, MATES } from "./edo-hills.js";
import { url } from "../../engine/assets.js";

const art = "art/scenes/edo-storehouse/";

// ---------- the room (layout.json: horizon 285, full 480; a grown-up 147 px inside the door, about 200 at the front edge) ----------
const WALK = [[286, 412], [430, 412], [438, 422], [539, 433], [546, 441], [597, 500], [614, 554], [729, 604], [26, 604], [188, 511], [264, 433], [304, 431],
  [311, 421], [279, 421]];
const BLOCKED = [[[500, 437], [546, 437], [524, 414], [485, 414]], [[257, 431], [304, 431], [319, 409], [278, 409]]];
const M = { door: [526, 464], windowIn: [486, 361], sacks: [455, 433], mat: [396, 445], trapdoor: [460, 445], lantern: [320, 430], isuke: [505, 471],
  default: [345, 480], bigsis: [344, 456], lilsis: [427, 430] };
/** Little Sister on top of the sacks under the window (the layout's stand `windowIn`: 90 cm up, drawn at 0.671), sorted in
    front of them; and the floor she hops down to (set by eye: the nearest floor in front of the pile). */
const ON_SACKS = { at: [486, 361], scale: 0.671, base: 423 };
const HOP = [450, 452];
/** The heap of sacks over the mat (#27): its ground (the layout's `solid` of sacks-heaped). */
const HEAP = [[350, 457], [447, 457], [439, 430], [358, 430]];
/** Where the other two come in, when Little Sister has lifted the bar: in at the door and along to these (set by eye). */
const IN = { mom: [492, 486], bigsis: [536, 500] };
/** The door's shape (shut; the opening, when it stands open) and the trapdoor's, flush with the floor (the layout's things). */
const DOOR = [[590, 478], [556, 443], [556, 304], [590, 308]];
const TRAP = [[363, 458], [428, 458], [424, 434], [369, 434]];
/** Coming up the ladder: the others round the trapdoor (set by eye, clear of the open lid and of the heap). */
const UP = [[430, 474], [486, 470]];

// ---------- what the room is doing now that is not saved (made again whenever the scene is built) ----------
const here = { dark: false, peeked: {} };

// ---------- the states of the cut-outs, from the story ----------
/** The lantern on its hook: put out the moment they came up the path, lit again from the night they are trusted. */
const lit = (g) => is(g, "edo.trusted");
/** The front door: open from the bar lifted until the morning (the family's way in and out); in the morning Jinsuke keeps it
    shut, and opens it to the constable (edo.isukeIn). */
const doorOpen = (g) => (is(g, "edo.unbarred") && !is(g, "edo.watch")) || is(g, "edo.isukeIn");
/** The sacks heaped over the mat over the trapdoor (#27), until he has gone. */
const heaped = (g) => is(g, "edo.sacksHid") && !sunUp(g);
/** The mat pulled aside off the trapdoor: from the moment it is moved (#25) until the sacks go over it (#27). */
const matAside = (g) => is(g, "edo.matMoved") && !heaped(g);
/** The trapdoor open, the ladder's top and the lamplight under it: from the first time down until the heap goes over it. */
const trapOpen = (g) => is(g, "edo.hidden") && !heaped(g);
/** The lamplight of the room below, up between the boards (and out for a moment when they knock on the trapdoor). By day, in
    the morning, nothing as faint as a lamp shows through: only her flashlight, pointing straight up (pinkOn). */
const warm = (g) => !here.dark && !is(g, "edo.watch");

// ---------- #25: the bar, the mat, the knock, the way down ----------
/** Little Sister, in alone, lifts the bar (the door's use or the bar's, before it is up), and the others come in. */
async function unbar(g) {
  const me = who(g);
  if (me !== "lilsis") return g.say(`edo.store.door.use.${me}`);             // (nobody else is ever in here with the bar across)
  g.lead.face("E");
  await g.reach();
  g.sfx("bar");
  await g.say("edo.store.door.use.lilsis");
  g.flag("edo.unbarred", true);
  g.sfx("shutter");
  g.follow();
  // Mom and Big Sister in out of the rain (they were on the path, at the door: edo-cedars.js), and along the wall
  for (const id of ["mom", "bigsis"]) {
    if (sceneOf(g, id) !== "edo-cedars") continue;
    await g.putLead(id, "edo-storehouse", STORE.doorway, { face: "W" });
    const f = g.actor(id);
    if (f) f.fade(0);
  }
  await Promise.all(["mom", "bigsis"].map(async (id, n) => {
    const f = g.actor(id);
    if (!f) return;
    await g.wait(450 * n);
    await Promise.all([g.tween(300, (k) => f.fade(k)), g.walkTo(IN[id][0], IN[id][1], id)]);
    f.face("NW");
  }));
  g.tidy();
}

/** The mat: with light at its edge. Little Sister alone in the room leaves it (the others are still outside); once they are in,
    whoever is played moves it, and under it is a door in the floor. */
async function mat(g) {
  const me = who(g);
  if (!is(g, "edo.unbarred")) return g.say(`edo.store.mat.${me}`);
  if (is(g, "edo.matMoved")) return g.say(g.fallback("nope"));
  await g.reach(true);
  g.flag("edo.matMoved", true);
  g.follow();
  await g.say(`edo.store.mat.use.${me}`);
  // "We should not open that." (Big Sister's own line has just said it, if she moved it) "No. We should knock."
  await g.say(...[me === "bigsis" ? null : "edo.store.mat.found.1", "edo.store.mat.found.2", "edo.store.mat.found.3", "edo.store.mat.found.4"]);
}

/** The trapdoor: knocked on (the light below goes out, and comes up again), and then down, slowly, and kind. After that it
    is the way down, and in the morning (#27) the way down until the heap goes over it. */
async function trapdoor(g) {
  const me = who(g), lead = g.lead;
  if (!is(g, "edo.knocked")) {
    if (lead) lead.face("W");
    await g.reach(true);
    g.sfx("knock");
    await g.wait(700);
    here.dark = true; g.follow();
    await g.say("edo.store.knock.1");
    await g.wait(900);
    here.dark = false; g.follow();
    await g.say("edo.store.knock.2", "edo.store.knock.3");
    g.flag("edo.knocked", true);
    return;
  }
  if (!is(g, "edo.hidden")) {
    await g.say(`edo.store.trapdoor.use.${me}`);
    g.sfx("trapdoor");
    g.flag("edo.hidden", true);
    g.follow();
    await g.wait(500);
    return g.goto("edo-chapel", { spawn: "ladder" });
  }
  g.sfx("trapdoor");
  return g.goto("edo-chapel", { spawn: "ladder" });
}

// ---------- #27: the sacks over the mat ----------
/** Big Sister and O-Rin put the mat back over the trapdoor and heap the sacks over it: eleven (Big Sister decides). A girl up
    here with her sister does it; Mom (who should be below) leaves them stacked, and so does anyone before the morning. */
async function hide(g) {
  const me = who(g);
  if (me === "mom" || sceneOf(g, "bigsis") !== "edo-storehouse") return g.say(`edo.store.sacks.use.${me}`);
  const big = g.actor("bigsis"), orin = g.actor("orin");
  await Promise.all([g.walkTo(M.sacks[0], M.sacks[1], "bigsis"), orin ? g.walkTo(410, 470, "orin") : null]);
  if (big) big.face("W");
  if (orin) orin.face("NE");
  if (big) big.fidget("count", { hold: true });
  await g.say("edo.store.hide.1", "edo.store.hide.2");
  await g.say("edo.store.hide.3");
  if (big) big.fidget(null);
  await g.fade(1, 350);
  g.sfx("trapdoor");
  g.flag("edo.sacksHid", true);
  g.follow();
  clearOf(g, HEAP, { bigsis: [462, 470], lilsis: [430, 486], mom: [380, 482], orin: [330, 470], jinsuke: STORE.jinsuke });
  if (orin) { orin.place(STORE.orin[0], STORE.orin[1]); orin.face("E"); }
  g.tidy();
  await g.wait(250);
  await g.fade(0, 350);
  await afterStep(g);
}
/** The sacks over the trapdoor: through them (they are shifted, the girls go down or come up, and they go back: O-Rin counts),
    while the constable is not in the room. */
async function throughPile(g) {
  if (is(g, "edo.isukeIn") || is(g, "edo.constableGone")) return g.say(`edo.store.sacks.use.${who(g)}`);
  if (who(g) === "mom" && is(g, "edo.isukeAtDoor")) return g.say("edo.store.isuke.use.mom");
  await g.fade(1, 300);
  g.sfx("trapdoor");
  passing.by = "pile";
  return g.goto("edo-chapel", { spawn: "ladder", via: "cut" });
}
/** The pile of sacks under the window, or the heap: the hide, the way through, or the sacks' own lines. */
function sacks(g) {
  if (morning(g) && !is(g, "edo.sacksHid")) return hide(g);
  if (heaped(g)) return throughPile(g);
  return g.say(`edo.store.sacks.use.${who(g)}`);
}

// ---------- #27: the pink light between the boards ----------
/** Her flashlight is on below, pointing up: Mom and Big Sister cannot turn it off from up here (their lines say whose it is);
    Little Sister goes down to it (edo-chapel.js: "Sorry, light."), over the trapdoor or through the sacks. */
async function pinkUse(g) {
  const me = who(g);
  await g.say(`edo.store.floorgaps.pink.use.${me}`);
  if (me !== "lilsis") return;
  passing.by = heaped(g) ? "pinkPile" : "pink";
  if (heaped(g)) { await g.fade(1, 300); g.sfx("trapdoor"); return g.goto("edo-chapel", { spawn: "ladder", via: "cut" }); }
  await g.walkTo(M.trapdoor[0], M.trapdoor[1]);
  g.sfx("trapdoor");
  return g.goto("edo-chapel", { spawn: "ladder" });
}

// ---------- #27: the door, Jinsuke, the constable ----------
/** The door in the morning. Before he is at it: a look out through the crack (the path, and him on it, a step nearer each time
    something is done), and Jinsuke's reason not to open yet (talk/edo-b.js NOT_READY). After his knock: answer it. */
async function door(g) {
  if (!morning(g)) {
    if (!is(g, "edo.unbarred")) return unbar(g);
    return g.say(who(g) === "lilsis" ? "edo.cedars.door.open.lilsis" : `edo.store.door.use.${who(g)}`);   // (hers: she opened it)
  }
  if (is(g, "edo.isukeIn")) return g.say(`edo.store.jinsuke.use.${who(g)}`);
  if (is(g, "edo.isukeAtDoor")) return talkToIsuke(g);
  await peek(g);
}
async function peek(g) {
  const me = who(g), step = isukeAt(g);
  if (here.peeked[me] !== step) {                                              // (a look out each time he has come a step nearer)
    here.peeked[me] = step;
    if (g.lead) g.lead.face("E");
    await g.wait(200);
    await toPath(g, async (g, man) => {
      await g.wait(500);
      await g.say(`edo.cedars.isuke.${me}`);
      if (man) await man.fidget("yawn");
      await g.wait(300);
    }, { at: ISUKE_WAY[step], face: "N" });
    await g.say(`edo.cedars.isuke.use.${me}`);
  }
  if (me !== "mom") await notReady(g);
}
/** Jinsuke by the door: busy keeping it. While the constable is in, what each of them makes of that; Mom, up here before he
    comes, waits till he has gone; the girls get his reason, or, once the room is ready and he has knocked, the door. */
async function jinsuke(g) {
  const me = who(g);
  if (is(g, "edo.isukeIn") || me === "mom") return g.say(`edo.store.jinsuke.use.${me}`);
  if (is(g, "edo.isukeAtDoor")) return talkToIsuke(g);
  return notReady(g);
}
/** O-Rin by the lantern, watching the door: she helps with the sacks (with Big Sister there); else a look at her. */
function orin(g) {
  if (morning(g) && !is(g, "edo.sacksHid") && who(g) !== "mom" && sceneOf(g, "bigsis") === "edo-storehouse") return hide(g);
  return g.say(`edo.chapel.orin.${who(g)}`);
}

// ---------- the scene ----------
export default {
  id: "edo-storehouse",
  era: "edo",
  name: "Inside the storehouse",
  // (no `music`: the era's own track, `edo`; the rain on the thatch is the loud thing in here)

  horizon: 285, full: 480, maxScale: 1.3,
  walk: { area: WALK },
  blocked: BLOCKED,
  spawn: { ...M },
  // in at the door: the other two beside whoever leads; up the ladder: round the trapdoor
  arrive: { door: [[496, 480], [548, 496]], trapdoor: UP },
  facing: "W",
  // before the bar is lifted Little Sister is in here alone (the others wait on the path); in the morning the girls go
  // together and Mom alone (edo-hills.js partyOf)
  party: (g) => (is(g, "edo.unbarred") ? partyOf(g) : []),
  exits: ["edo-cedars", "edo-chapel"],
  stock: STOCK_DRESSED,
  talk: TALK,

  picture: art + "back.png",
  // Back to front, as the painter lists them (the light between the boards before the mat).
  planes: [
    { id: "lantern", states: { out: art + "lantern.png", lit: art + "lantern-lit.png" }, state: (g) => (lit(g) ? "lit" : "out"), plane: "back" },
    { id: "sacks", src: art + "sacks.png", base: [[438, 421], [534, 421]], solid: [[438, 422], [535, 422], [523, 410], [435, 410]], when: (g) => !heaped(g) },
    { id: "sacks-heaped", src: art + "sacks-heaped.png", base: [[352, 457], [448, 457]], solid: HEAP, when: heaped },
    { id: "door", states: { shut: art + "door.png", open: art + "door-open.png" }, state: (g) => (doorOpen(g) ? "open" : "shut"), plane: "back" },
    { id: "bar", states: { across: art + "bar.png", up: art + "bar-up.png" }, state: (g) => (is(g, "edo.unbarred") ? "up" : "across"), plane: "back" },
    { id: "trapdoor", states: { shut: art + "trapdoor.png", open: art + "trapdoor-open.png" }, state: (g) => (trapOpen(g) ? "open" : "shut"), plane: "back" },
    { id: "floorgaps-on", src: art + "floorgaps-on.png", plane: "back", when: warm },
    { id: "mat", states: { down: art + "mat.png", aside: art + "mat-aside.png" }, state: (g) => (matAside(g) ? "aside" : "down"), plane: "back" },
    { id: "near", src: art + "near.png", plane: "front" },
  ],
  // Her flashlight's light up between the boards (#27): the painter's warm light between the boards, turned pink, on the
  // live layer (over the painting, under every cut-out: the mat, the lid, the heap), while it is on below.
  live: (kit, g) => `<defs><filter id="edo-pink" color-interpolation-filters="sRGB"><feColorMatrix type="matrix"
      values="1 0 0 0 0.05  0.25 0.25 0 0 0  0.35 0.35 0.35 0 0.12  0 0 0 1.15 0"/></filter></defs>
    <image id="edo-pinkgaps" href="${url(art + "floorgaps-on.png")}" width="800" height="600" filter="url(#edo-pink)" opacity="${pinkOn(g) ? 1 : 0}"/>`,
  // ENGINE-20: the rain loud on the thatch (the window's rain, its sound at full: level 1), and in the doorway while it is open.
  fx: [
    { id: "rain-window", type: "rain", when: raining, plane: "back", area: [[430, 278], [466, 278], [466, 313], [430, 313]], slant: 8, count: 8, length: [6, 12],
      speed: 420, color: "#dfe6ec", opacity: 0.45, sound: "rain", level: 1 },
    { id: "rain-door", type: "rain", when: (g) => raining(g) && doorOpen(g), plane: "back", area: [[558, 310], [588, 315], [588, 476], [558, 445]], slant: 8,
      count: 18, length: [10, 20], speed: 520, color: "#dfe6ec", opacity: 0.4, sound: false },
  ],

  // #27: Jinsuke keeps the door (beside it; while the constable is in, between him and the girls), O-Rin watches by the
  // lantern, and the constable stands dripping inside the door while he asks (PEOPLE-20's kinds).
  actors: [
    { id: "jinsuke", kind: "jinsuke", at: STORE.jinsuke, face: "W", when: (g) => is(g, "edo.watch") && !is(g, "edo.mirror") && !is(g, "edo.isukeIn"), life: { fidget: [5, 10] } },
    { id: "jinsuke", kind: "jinsuke", at: STORE.guard, face: "E", when: (g) => is(g, "edo.isukeIn"), life: { fidget: [6, 12] } },
    { id: "orin", kind: "orin", at: STORE.orin, face: "E", when: (g) => is(g, "edo.watch") && !is(g, "edo.mirror"), life: { fidget: [4, 9] } },
    { id: "isuke", kind: "isuke", at: STORE.isuke, face: "W", when: (g) => is(g, "edo.isukeIn"), life: { fidget: [3, 7] } },
  ],

  // Back to front: a later area lies over an earlier one (the other two first: edo-hills.js MATES).
  hotspots: [
    ...MATES,
    { id: "window", name: "high window", poly: [[430, 313], [466, 313], [466, 278], [430, 278]], walkTo: M.sacks, face: "N",
      look: each("edo.store.window"), use: each("edo.store.window.use") },
    { id: "tools", name: "tools", poly: [[359, 275], [371, 275], [371, 340], [359, 340]], walkTo: [362, 424], face: "N",
      look: each("edo.store.tools"), use: each("edo.store.tools.use") },
    { id: "lantern", name: "paper lantern", rect: [254, 303, 28, 48], walkTo: M.lantern, face: "W",
      look: (g) => g.say(lit(g) ? `edo.store.lantern.lit.${who(g)}` : `edo.store.lantern.${who(g)}`),
      use: (g) => g.say(lit(g) ? g.fallback("nope") : `edo.store.lantern.use.${who(g)}`) },
    { id: "straw", name: "straw rope", poly: [[545, 346], [532, 340], [532, 312], [545, 315]], walkTo: [512, 438], face: "E", when: (g) => !doorOpen(g),      // (behind the door, when it stands open)
      look: each("edo.store.straw"), use: each("edo.store.straw.use") },
    { id: "baskets", name: "baskets", poly: [[506, 435], [541, 435], [522, 415], [491, 415]], walkTo: [478, 438], face: "E", when: (g) => !doorOpen(g),     // (behind the open door too)
      look: each("edo.store.baskets"), use: each("edo.store.baskets.use") },
    { id: "door", name: "door", poly: DOOR, walkTo: M.door, face: "E", when: (g) => !is(g, "edo.unbarred"), look: each("edo.store.door"), use: door, verb: "Unbar" },
    { id: "door-shut", name: "door", poly: DOOR, walkTo: M.door, face: "E", when: (g) => is(g, "edo.unbarred") && !doorOpen(g), look: each("edo.store.door"), use: door, verb: "Open" },
    { id: "door-open", name: "door", poly: [[493, 470], [553, 446], [553, 306], [493, 312]], walkTo: M.door, face: "E", when: doorOpen,
      look: each("edo.store.door"), use: door },
    { id: "doorway", name: "the path", poly: DOOR, walkTo: M.door, face: "E", verb: "Go out to",
      when: (g) => doorOpen(g) && !is(g, "edo.isukeIn"), use: (g) => g.goto("edo-cedars", { spawn: "door" }), look: (g) => g.say(`edo.cedars.rain.${who(g)}`) },
    { id: "bar", name: "bar", poly: [[589, 410], [549, 384], [549, 366], [589, 388]], walkTo: M.door, face: "E",
      look: each("edo.store.bar"), use: (g) => (is(g, "edo.unbarred") ? g.say(`edo.store.bar.use.${who(g)}`) : unbar(g)) },
    { id: "sacks", name: "charcoal sacks", poly: [[437, 423], [531, 423], [531, 372], [502, 356], [462, 358], [437, 374]], walkTo: M.sacks, face: "N", when: (g) => !heaped(g),
      look: (g) => g.say(`edo.store.sacks.${who(g)}`), use: sacks },
    { id: "heap", name: "charcoal sacks", poly: [[352, 458], [448, 458], [452, 430], [436, 398], [392, 392], [360, 404], [350, 432]], walkTo: [404, 470], face: "N", when: heaped,
      look: (g) => g.say(`edo.store.sacks.hid.${who(g)}`), use: sacks },
    { id: "floorgaps", name: "floorboards", poly: [[296, 487], [504, 487], [468, 418], [332, 418]], walkTo: [400, 476], face: "N",
      when: (g) => warm(g) || pinkOn(g),
      look: (g) => g.say(pinkOn(g) ? `edo.store.floorgaps.pink.${who(g)}` : `edo.store.floorgaps.${who(g)}`),
      use: (g) => (pinkOn(g) ? pinkUse(g) : g.say(`edo.store.floorgaps.use.${who(g)}`)) },
    { id: "mat-aside", name: "straw mat", poly: [[239, 457], [354, 457], [346, 425], [247, 425]], walkTo: [300, 466], face: "W", when: matAside,
      look: (g) => g.say(g.fallback("look")), use: (g) => (morning(g) ? sacks(g) : g.say(g.fallback("nope"))) },
    { id: "mat", name: "straw mat", poly: [[341, 464], [450, 464], [441, 430], [352, 430]], walkTo: M.mat, face: "N", when: (g) => !is(g, "edo.matMoved"),
      look: each("edo.store.mat"), use: mat, verb: "Move" },
    { id: "trapdoor", name: "trapdoor", poly: TRAP, walkTo: M.trapdoor, face: "W", when: (g) => is(g, "edo.matMoved") && !is(g, "edo.knocked"),
      look: each("edo.store.trapdoor"), use: trapdoor, verb: "Knock on" },
    { id: "trapdoor-shut", name: "trapdoor", poly: TRAP, walkTo: M.trapdoor, face: "W", when: (g) => is(g, "edo.knocked") && !trapOpen(g) && !heaped(g),
      look: each("edo.store.trapdoor"), use: trapdoor, verb: "Open" },
    { id: "trapdoor-open", name: "trapdoor", poly: [[351, 463], [441, 463], [436, 380], [356, 380]], walkTo: M.trapdoor, face: "W", when: trapOpen,
      look: each("edo.store.trapdoor"), use: trapdoor, verb: "Go down" },
    // the people (#27)
    { id: "orin", name: "O-Rin", rect: [310, 362, 40, 110], walkTo: [372, 476], face: "W", when: (g) => is(g, "edo.watch") && !is(g, "edo.mirror"),
      look: (g) => g.say(`edo.chapel.orin.${who(g)}`), use: orin, verb: "Talk to" },
    { id: "jinsuke", name: "Jinsuke", rect: [466, 296, 48, 168], walkTo: [452, 476], face: "E", when: (g) => is(g, "edo.watch") && !is(g, "edo.mirror") && !is(g, "edo.isukeIn"),
      look: (g) => g.say(`edo.store.jinsuke.${who(g)}`), use: jinsuke, verb: "Talk to" },
    { id: "jinsuke-guard", actor: "jinsuke", name: "Jinsuke", rect: [428, 304, 48, 170], walkTo: [404, 482], face: "E", when: (g) => is(g, "edo.isukeIn"),
      look: (g) => g.say(`edo.store.jinsuke.${who(g)}`), use: jinsuke, verb: "Talk to" },
    { id: "isuke", name: "the constable's man", rect: [481, 303, 48, 168], walkTo: null, face: "E", when: (g) => is(g, "edo.isukeIn"),      // (talked to from where she stands)
      look: (g) => g.say(`edo.store.isuke.${who(g)}`), use: talkToIsuke, verb: "Talk to" },
  ],

  setup(g) {
    here.dark = false;
    hats(g, false);                                                            // (indoors: the hats on their backs)
    keepBelow(g);
    // Little Sister in by the window: on top of the sacks under it, before the picture comes up (enter hops her down)
    if (passing.by === "window" && g.lead) { const l = g.lead; l.place(ON_SACKS.at[0], ON_SACKS.at[1], ON_SACKS.scale); l.base = ON_SACKS.base; l.face("S"); }
    const pinkEl = g.q("#edo-pinkgaps");
    if (pinkEl) pinkEl.setAttribute("opacity", pinkOn(g) ? "1" : "0");
  },

  async enter(g, from) {
    const way = passing.by;
    passing.by = null;
    // #25: in through the window, onto the sacks: alone in a stranger's dark storehouse, and pleased about it
    if (way === "window") {
      const l = g.lead;
      await g.say("edo.cedars.window.in.2", "edo.cedars.window.in.3");
      if (l) {
        const [x0, y0] = ON_SACKS.at;
        await g.tween(520, (k) => l.place(x0 + (HOP[0] - x0) * k, y0 + (HOP[1] - y0) * k - 26 * Math.sin(Math.PI * k), ON_SACKS.scale + (g.sizeAt(HOP[0], HOP[1]) - ON_SACKS.scale) * k));
        l.base = null;
        g.rememberPlace();
      }
      return;
    }
    if (way === "pile" || way === "pinkPile") await g.say("edo.store.pile.orin");     // (the sacks shifted for her, and put back)
    if (!morning(g)) return;
    // Mom up here in the morning: the one place he will look
    if (who(g) === "mom" && from === "edo-chapel") { await g.say("edo.chapel.watch.5"); return; }
    // he has knocked, and a girl comes up: she answers it
    if (is(g, "edo.isukeAtDoor") && !is(g, "edo.isukeIn") && GIRLS.includes(who(g)) && from === "edo-chapel") await talkToIsuke(g);
  },
};

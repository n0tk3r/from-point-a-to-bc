// Act Six, the third leg: the top floor of the keep at Himeji, at sunset (SCENES-20C: new in round twenty, in place of
// ENGINE-20's sketch; briefs/SCENES-20.md, and the design, briefs/out/edo-design.md, "edo-keeptop" and #30). A plain room of
// dark wood, a window bay shuttered in the middle of each wall (the south one behind the camera); the hum in the east wall,
// a shimmer in the air the player can learn to see; dust; an old lantern nobody has lit in years. Through the west window,
// once it is opened, the sun going down over the town and the Inland Sea, and the herons going past.
//
// The three of them come up the stairs behind the warden and the pink light (edo-keep.js, the climb), at the mark `stairs`,
// Mom leading: "Six. The top, girls."
//
//   #30 The Lady Of The Keep      (1) the truth: in the half dark, a tall woman with a mirror held up; Shinnosuke falls to
//                                 his knees (topTree, js/content/talk/edo-b.js: his truth first, then "Are you the lady of
//                                 the keep?"); Mom tells him hers (edo.truth). (2) the window: the bar is the warden's to
//                                 lift; asked properly, he lifts it, and the low sun fills the room (edo.window). (3) the
//                                 mirror on the hum: a hand-sized patch of light, a letterbox of a door (edo.letterbox; the
//                                 doorTree's lines); Big Sister: the farther, the bigger. Then the player backs Mom away
//                                 across the floor, step by step (the floor, while she holds the light), or all the way (the
//                                 west window), the patch and the door growing at every step, into the mouth of the window:
//                                 a doorway, the cross in it (edo.doorway). (4) the coin into Mom's hand (at once, if she has
//                                 it; else whoever holds it gives it to her: handed over, or asked for), and the mirror into
//                                 the warden's hands, for Tomezō (edo.door). Then the cut-scene "Hold Hands" (edo-step.js),
//                                 and the title: the end of the demo.
//   wrong tries                   the west shutters before he has lifted the bar (the bar is his); the other shutters (not
//                                 the window we need); the mirror on the hum in the dark; the coin on it (for steering, not
//                                 for opening); the lantern (no fire in a wooden keep).
//
// The trees are WRITE-20B's, with these changes of staging made here (ready.md lists them): in topTree the girls' words to
// the kneeling warden end the talk (it had no way out for them); the doorTree is played in three goes, the player doing what
// is between them (backing Mom away; giving her the coin), its lines in its order, "A plate. A lid. A door." said on the way
// back; when Mom has not the coin at the window she says so (her hint's line), and it is handed to her.
//
// The light is ENGINE-20's `mirror` kind driving a `portal` (the door), at the painter's numbers (layout.json `hum`, `door`,
// `patch`): the patch a twelfth of a metre across at the wall, two at the window, squeezed as the wall is seen (the door's
// `wide`, 0.6); the engine's `fit: "height"` (a small change made for this, effects.js, marked) makes the door's rings reach
// the patch's edge both ways.
//
// Every place is the painter's own measurement of the finished picture (art/scenes/edo-keeptop/layout.json, PAINT-20E's
// ready.md), or was set by eye against the picture with the people in it; where the two differ the comment says why.
//
// Try it: index.html?scene=edo-keeptop&lead=mom&flags=edo.walked,edo.tomezoDown,edo.trowelBack,edo.crew,edo.inside,edo.shinMet,edo.lightShown,edo.up,edo.climbed

import { STOCK_DRESSED } from "./edo-common.js";
import { THREE, who, is, heard, each, walkBack, holderOf, moveItem, TALK } from "./edo-himeji.js";
import { topTree, doorTree, CLIMB } from "../talk/edo-b.js";

const art = "art/scenes/edo-keeptop/";

// ---------- the camera and the floor (layout.json: horizon 270, full 430; the lens 175 cm up in the south bay) ----------
const HORIZON = 270, FULL = 430;
const FLOOR = [[194, 367], [598, 367], [799, 470], [183, 470], [210, 445], [30, 445]];

// ---------- the marks (layout.json marks) ----------
const M = { stairs: [217, 464], shinnosuke: [278, 450], west: [91, 433], south: [400, 464], north: [400, 371], east: [670, 422],
  hum: [617, 389], m1: [536, 402], m2: [416, 410], m3: [281, 419], farwest: [82, 422], mid: [417, 422] };
/** Mom's way back from the wall with the mirror, mark by mark (layout.json `patch`: the patch's size at each). */
const WAY_BACK = ["hum", "m1", "m2", "m3", "farwest"];
const TO_WARDEN = [318, 454];          // where whoever talks to the warden stands: a pace to his right, turned to him
const BESIDE_MOM = [122, 440];         // the warden, come over to Mom in the window's mouth for the mirror
const MOM_OUT = [214, 446];            // Mom, out of the window's mouth when the mirror is in his hands
const MOUTH = [84, 424];               // the warden in the window's mouth with the mirror, keeping its light on the hum
const ASIDE = { bigsis: [470, 446], lilsis: [372, 452] };      // the girls, out of the light's way, watching it grow

// ---------- the hum, the door and the light (layout.json `hum`, `door`, `patch`) ----------
const HUM = [641, 295];
const HUM_POLY = [[655, 295], [653, 306], [648, 314], [641, 317], [635, 314], [630, 306], [628, 295], [630, 284], [635, 276], [641, 273], [648, 276], [653, 284]];
const HUM_K = 0.6;                     // how far the hum's own shimmer is open, once someone has looked at it long enough
// The patch: the painter gives its height's radius by the distance of the holder's feet from the hum (8.6 px at `hum`, 64 at
// `farwest`); the engine measures from the mirror (the hand: [18, 100] at full size, ahead of the feet) and takes the patch's
// width's radius. So: the same two patches, by the hand's distance (22.3 px at `hum`, 542.8 at `farwest`), each 0.6 as wide
// as it is high (the wall seen from the side, as the door's `wide`).
const WIDE = 0.6;
const SIZES = [[22.3, 8.6 * WIDE], [542.8, 64 * WIDE]];

// ---------- the story, as the picture shows it ----------
const lit = (g) => is(g, "edo.window");                                         // the west shutters open: the sun in
const holding = (g) => is(g, "edo.letterbox") && !is(g, "edo.door");            // Mom with the mirror's light on the hum
const momUp = (g) => (is(g, "edo.knelt") && !is(g, "edo.truth")) || holding(g);  // Mom with the mirror held up
const humSeen = (g) => THREE.some((id) => heard(g, `edo.top.hum.${id}`));        // the hum looked at long enough to see it
const coinTime = (g) => is(g, "edo.doorway") && !is(g, "edo.door");             // the doorway open, the coin not yet given
const warden = (g) => g.actor("shinnosuke");
// The other shutters stay shut in the story (only the west one is the warden's to open tonight; WRITE-20B's ids.md: "the
// others are there if a script opens them"): openShutter(g, side) opens one for a script, and its looks follow.
const OPENED = { north: false, east: false, south: false };
const opened = (g, side) => (side === "west" ? lit(g) : OPENED[side]);
export function openShutter(g, side, on = true) {
  if (!(side in OPENED)) return;
  OPENED[side] = !!on;
  g.sfx("shutter");
  g.view.cast.refresh(g);
  relight(g);
}

/** The doors in the wall read the paint again (the room lit, a shutter opened: the lit wall is bent, not the dark one). */
function relight(g) { for (const id of ["hum", "door"]) { const d = g.effects.get(id); if (d && d.refresh) d.refresh(); } }
/** The hum's own shimmer: open while it has been seen and the light is not on it (then the door is there instead). */
function shimmer(g, ms = 0) {
  const h = g.effects.get("hum");
  if (!h) return Promise.resolve();
  const want = humSeen(g) && !is(g, "edo.letterbox") ? HUM_K : 0, from = h.openK || 0;
  if (!ms || g.clock.skipping) { h.open(want); return Promise.resolve(); }
  return g.tween(ms, (k) => h.open(from + (want - from) * k));
}
/** The hum, heard: a low sound, quiet as they come up, louder once it is seen, in the sun, and as the door opens. */
const humLevel = (g) => (is(g, "edo.doorway") ? 1.8 : is(g, "edo.letterbox") ? 1.4 : lit(g) ? 1.1 : humSeen(g) ? 0.9 : 0.6);
const room = { hum: null };

// ---------- #30 (1) and (2): the truth, and the window (topTree) ----------
/** The hook `kneel`: he goes down on his knees to her. */
async function kneel(g) {
  const sh = warden(g), mom = g.actor("mom");
  if (!sh) return;
  if (mom) sh.look(mom.x, mom.y);
  if (sh.act && sh.act.low === "light") sh.hold(false);
  sh.kneel(true);
  await g.wait(560);                                  // (the rig eases him down over about half a second)
}
/** The hook `stand`: he gets up, the light in his hands again (and Mom lowers the mirror: she is nobody's lady). */
async function stand(g) {
  const sh = warden(g);
  if (sh && sh.kneeling) { sh.kneel(false); await g.wait(420); }
  if (sh && !(sh.act && sh.act.low === "light")) sh.hold(true, "light");
  if (g.dressOf("mom") === "edo-crew-mirror" && !holding(g)) g.dress("mom", "edo-crew");
}
/** The hook `window`: he goes to the west bay and lifts the bar, and the shutters swing open; the low sun fills the room
    ("It came in all at once"). Then back to his place at the stairs. */
async function openWest(g) {
  const sh = warden(g);
  if (sh) {
    sh.hold(false);
    await g.walkTo(M.west[0], M.west[1], "shinnosuke");
    sh.face("W");
    await sh.play(g.clock, "reach");
  }
  g.sfx("bar");
  await g.wait(450);
  g.sfx("shutter");
  g.flag("edo.window", true);                     // (the tree sets it too, after this hook: the room is lit as the shutters swing)
  relight(g);
  await g.wait(350);
  if (sh) {
    await g.walkTo(M.shinnosuke[0], M.shinnosuke[1], "shinnosuke");
    sh.face("E");
    sh.hold(true, "light");
  }
}
const TOP = (() => {
  const t = topTree({ kneel, stand, window: openWest });
  // (staging) the girls' words to the kneeling warden end the talk: theirs are the only buttons there for them, and a menu
  // whose only buttons are clues has no way out.
  for (const o of t.nodes.kneeling.options) if (o.id === "bigsis" || o.id === "lilsis") o.then = "exit";
  return t;
})();
async function wardenUse(g) {
  const sh = warden(g), lead = g.lead;
  if (sh && lead && !(sh.act && sh.act.low === "kneel")) sh.look(lead.x, lead.y);
  await g.talk(TOP);
}

/** Coming up, the first time: Mom says the sixth floor; she takes the grandmother's mirror out and holds it up to what light
    there is in the cracks: in the half dark, a tall woman with a mirror. He turns with the pink light and falls to his knees,
    and tells her the truth first, as the story says, and asks: is she the lady of the keep? (topTree's `kneel` and `ask`.)
    Then the player has the controls, the question hanging: the answer is Mom's to give (a click on him: `kneeling`). */
const TOP_ARRIVAL = { ...TOP, start: "kneel", nodes: { ...TOP.nodes, ask: { ...TOP.nodes.ask, then: "exit" } } };
async function arrive(g) {
  const mom = g.actor("mom"), sh = warden(g);
  await g.wait(400);
  if (mom) mom.face("E");
  await g.say(CLIMB[CLIMB.length - 1]);
  if (holderOf(g, "mirror") === "mom" && g.dressOf("mom") !== "edo-crew-mirror") { g.dress("mom", "edo-crew-mirror"); g.sfx("click"); }
  await g.wait(600);
  if (sh && mom) sh.look(mom.x, mom.y);
  if (sh && sh.fidget) { const f = sh.fidget("tremble"); if (f && f.then) await f; }
  await g.talk(TOP_ARRIVAL);
}

// ---------- #30 (3) and (4): the mirror, the door, the coin (doorTree) ----------
/** The hook `patch`: Mom at the hum with the mirror held up in the sun; its light on the hum, a hand's size; the shimmer flares
    into rings: a letterbox of a door. The girls step out of the light's way to watch. */
async function letterbox(g) {
  const mom = g.actor("mom"), light = g.effects.get("light");
  if (mom && Math.hypot(mom.x - M.hum[0], mom.y - M.hum[1]) > 3) await g.walkTo(M.hum[0], M.hum[1], "mom");
  if (mom) mom.face("E");
  if (g.dressOf("mom") !== "edo-crew-mirror") g.dress("mom", "edo-crew-mirror");
  if (light) light.set({ holder: "mom", shown: false });
  const watch = ["bigsis", "lilsis"].map((id) => (g.actor(id) && Math.hypot(g.actor(id).x - ASIDE[id][0], g.actor(id).y - ASIDE[id][1]) > 30
    ? g.walkTo(ASIDE[id][0], ASIDE[id][1], id).then(() => { const a = g.actor(id); if (a) a.face("E"); }) : null));
  if (light) await g.tween(600, (k) => light.set({ on: k }));
  await shimmer(g, 300).then(() => { const h = g.effects.get("hum"); if (h) h.open(0); });
  g.sfx("portal");
  if (light) await g.tween(900, (k) => light.set({ doorK: k }));
  g.flag("edo.letterbox", true);
  await Promise.all(watch);
  g.rebuildSpots();
}
/** The next of Mom's marks back from the wall (the first one west of where she is), or -1 at the window. */
function nextBack(mom) {
  for (let i = 0; i < WAY_BACK.length; i++) if (M[WAY_BACK[i]][0] < mom.x - 8) return i;
  return -1;
}
/** Mom backs away from the wall with the light on it, a mark at a time (or all the way, from the west window): the patch and
    the door grow at every step. At the window's mouth: the doorway. */
async function backAway(g, all = false) {
  const mom = g.actor("mom");
  if (!mom || !holding(g) || is(g, "edo.doorway")) return;
  mom.face("E");
  let i = nextBack(mom);
  while (i >= 0 && i < WAY_BACK.length) {
    await walkBack(g, "mom", [M[WAY_BACK[i]]]);
    mom.face("E");
    if (WAY_BACK[i] === "m2" && !heard(g, GROWING[0])) await g.say(...GROWING);
    if (!all) break;
    i++;
  }
  if (Math.hypot(mom.x - M.farwest[0], mom.y - M.farwest[1]) < 3) await doorway(g);
}
/** In the mouth of the west window: the door a doorway, its rings out to the patch's edge, and in the middle of it, faint and
    clear, the cross. The doorTree's `grown` (from "I'm in the window"); then the coin, if Mom has it. */
async function doorway(g) {
  g.flag("edo.doorway", true);
  const light = g.effects.get("light");
  if (light) light.set({ shown: true });
  g.rebuildSpots();
  await g.wait(500);
  await g.talk({ ...DOOR, start: "grown" });
  if (is(g, "edo.door")) await theStep(g);
}
/** The coin into Mom's hand, from `from` (it has been handed over already, or is handed now by the hook): the doorTree from
    the giver's line (coinBig, coinLil) to the mirror in the warden's hands. */
const COIN = { from: null };
async function coinToMom(g, from) {
  if (!coinTime(g)) return;
  COIN.from = from;
  await g.talk({ ...DOOR, start: from === "lilsis" ? "coinLil" : "coinBig" });
  if (is(g, "edo.door")) await theStep(g);
}
/** The hook `coin`: the giver puts it in Mom's hand (unless it is there already: handed over). */
async function coinHook(g) {
  if (holderOf(g, "coin") === "mom") return;
  const from = COIN.from || holderOf(g, "coin"), a = from ? g.actor(from) : null, mom = g.actor("mom");
  if (a && mom) { a.look(mom.x, mom.y); await a.play(g.clock, "reach"); }
  moveItem(g, "coin", "mom");
  g.sfx("pickup");
  if (!g.clock.skipping) g.ui.toast("Mom has the coin");
}
/** The hook `giveMirror`: the warden comes over to her in the window's mouth; the mirror into his hands, and its light with it
    (he keeps it on the hum); she steps out of the mouth and he backs into it. The mirror is his to carry down, for Tomezō. */
async function giveMirror(g) {
  const sh = warden(g), mom = g.actor("mom"), light = g.effects.get("light");
  if (sh) {
    sh.hold(false);
    await g.walkTo(BESIDE_MOM[0], BESIDE_MOM[1], "shinnosuke");
    if (mom) sh.look(mom.x, mom.y);
  }
  if (mom) await mom.play(g.clock, "reach");
  const inv = g.store.data.inventory, from = holderOf(g, "mirror");
  if (from) { inv[from].splice(inv[from].indexOf("mirror"), 1); g.store.emit(); }
  g.sfx("pickup");
  if (g.dressOf("mom") !== "edo-crew") g.dress("mom", "edo-crew");
  if (sh) { sh.face("E"); sh.hold(true, "mirror"); }
  if (light) light.set({ holder: "shinnosuke" });                      // (no word on the screen: the step follows at once, and its card)
  if (mom) { await g.walkTo(MOM_OUT[0], MOM_OUT[1], "mom"); mom.face("E"); }
  if (sh) { await walkBack(g, "shinnosuke", [MOUTH]); sh.face("E"); }
}
const GROWING = [];                       // "A plate. A lid. A door. Keep GOING, Mommy.": said on the way back
const DOOR = (() => {
  const t = doorTree({ patch: letterbox, back: () => {}, coin: coinHook, giveMirror });
  // (staging) three goes: the letterbox, and the player backs Mom away (the floor, the window: backAway); at the window the
  // doorway; and the coin, by whoever holds it (coinToMom), if Mom has it not.
  t.nodes.small.then = "exit";
  GROWING.push(t.nodes.grown.say[0]);
  t.nodes.grown.say = t.nodes.grown.say.slice(1);
  t.nodes.grown.then = async (g) => {
    if (holderOf(g, "coin") === "mom") return "coinMom";
    if (holderOf(g, "coin")) await g.say("hint.edo.door.mom.5");      // ("The coin steers. Whoever has your brother's coin...")
    return "exit";
  };
  return t;
})();
/** The mirror on the hum: in the dark, only bronze; in the sun, the letterbox (the doorTree, first go). Mom's to hold: if one
    of the girls has it, it goes back to Mom, and Mom takes over. */
async function humMirror(g) {
  if (!lit(g)) return g.say(`edo.top.hum.with.mirror.dark.${who(g)}`);
  if (is(g, "edo.letterbox")) return g.say(`hint.edo.door.${who(g)}${is(g, "edo.doorway") ? ".5" : ".4"}`);
  const me = who(g);
  if (me !== "mom") {
    moveItem(g, "mirror", "mom");
    await g.walkTo(560, 432, me);
    const d = g.store.data;
    if (g.lead && g.lead._stop) g.lead._stop();
    d.active = "mom";
    g.store.emit();
  }
  await g.talk(DOOR);
}
/** The cut-scene "Hold Hands" (edo-step.js), and the title: the end of the demo. */
async function theStep(g) {
  await g.cutscene("edo-step");
  if (is(g, "demo.done")) await g.title();
}

// ---------- the shutters, the hum, the floor ----------
const SIDE_LOOK = (side) => (g) => g.say(`edo.top.${side}shutter${opened(g, side) ? ".open" : ""}.${who(g)}`);
/** A shutter used: shut, the bar is the warden's (the west) or it is not the window we need (the others); open, what one does
    in it. While Mom holds the light, the west window is where she backs to, all the way. */
const SIDE_USE = (side) => (g) => {
  if (side === "west" && holding(g) && who(g) === "mom") return is(g, "edo.doorway") ? g.say("hint.edo.door.mom.5") : backAway(g, true);
  return g.say(`edo.top.${side}shutter${opened(g, side) ? ".open" : ""}.use.${who(g)}`);
};
async function humLook(g) {
  const first = !humSeen(g);
  await g.say(`edo.top.hum.${who(g)}`);
  if (first && !is(g, "edo.letterbox")) await shimmer(g, 2400);      // (looked at long enough, it is seen)
}
function humUse(g) {
  if (is(g, "edo.letterbox")) return g.say(`hint.edo.door.${who(g)}${is(g, "edo.doorway") ? ".5" : ".4"}`);
  return g.say(`edo.top.hum.use.${who(g)}`);
}
/** Mom holding the light: she stays where she is (the floor is "Back away across" for her, a step at a time). */
const momHolds = (g) => holding(g) && who(g) === "mom" && !is(g, "edo.doorway");

/** What the three say to one another up here: WRITE-20A's companion lines (edo-himeji.js); and, while the doorway is open and
    the coin is not in Mom's hand, a word between Mom and whoever has it is the coin given. */
const coinWord = (from) => (g) => (coinTime(g) && holderOf(g, "coin") === from ? [{ say: (gg) => coinToMom(gg, from) }] : null);
const TOP_TALK = {
  mom: { bigsis: (g) => coinWord("bigsis")(g) || TALK.mom.bigsis, lilsis: (g) => coinWord("lilsis")(g) || TALK.mom.lilsis },
  bigsis: { mom: (g) => coinWord("bigsis")(g) || TALK.bigsis.mom },
  lilsis: { mom: (g) => coinWord("lilsis")(g) || TALK.lilsis.mom, bigsis: TALK.lilsis.bigsis },
};

/** A thing of the room, by its shape, with a look and a use for each of the three. */
const thing = (id, name, shape, walkTo, face, more = {}) => ({ id, name, ...shape, walkTo, face, look: each(`edo.top.${id}`), use: each(`edo.top.${id}.use`), ...more });
const westBay = [[129, 331], [0, 359], [0, 158], [129, 195]];
const westOpen = [[174, 195], [174, 331], [129, 331], [0, 359], [0, 158], [129, 195]];      // (with its leaves folded back beside it)

export default {
  id: "edo-keeptop",
  era: "edo",
  name: "The top of the keep",
  music: "edo-keep",

  horizon: HORIZON, full: FULL,
  walk: { area: FLOOR },
  // the chests, the lantern's foot, the stairwell (layout.json blocked)
  blocked: [[[216, 362], [337, 362], [325, 379], [181, 379]], [[345, 366], [367, 366], [365, 371], [342, 371]], [[41, 449], [185, 449], [35, 574], [0, 574]]],

  party: THREE,
  spawn: { default: M.stairs, ...M },
  // Up the stairs before Mom (the climb's order: the warden, Little Sister, Big Sister, Mom): the girls a few steps in.
  arrive: { stairs: [[334, 424], [376, 452]] },
  facing: "E",
  stock: STOCK_DRESSED,
  talk: TOP_TALK,
  // Mom holding the light on the hum stays where she is: she backs away when the player says (the floor, the window).
  still: (g, id) => id === "mom" && holding(g),
  tick(g) {
    const want = humLevel(g);
    if (room.hum !== want && g.loop("hum", { level: want })) room.hum = want;
  },

  picture: art + "back.png",
  // CUT-OUTS (the painter's plan): the lit room is an alt over the whole stage (lit.png), with every cut-out's `-lit` twin; the
  // shutters behind everybody, the west one open in the lit room; the rail round the stairwell (its base its slanting foot),
  // the chests, the lantern; the beam across the front. Back to front.
  planes: [
    { id: "lit", src: art + "lit.png", plane: "back", when: lit },
    ...["north", "east"].map((side) => ({ id: `${side}shutter`, plane: "back",
      states: { shut: art + `${side}shutter.png`, lit: art + `${side}shutter-lit.png`, open: art + `${side}shutter-open.png`, "open-lit": art + `${side}shutter-open-lit.png` },
      state: (g) => (opened(g, side) ? (lit(g) ? "open-lit" : "open") : lit(g) ? "lit" : "shut") })),
    { id: "westshutter", plane: "back", states: { shut: art + "westshutter.png", open: art + "westshutter-open.png", "open-lit": art + "westshutter-open-lit.png" },
      state: (g) => (lit(g) ? "open-lit" : "shut") },
    { id: "rail", states: { shut: art + "rail.png", lit: art + "rail-lit.png" }, state: (g) => (lit(g) ? "lit" : "shut"), base: [[34, 568], [177, 452]] },
    { id: "chests", states: { shut: art + "chests.png", lit: art + "chests-lit.png" }, state: (g) => (lit(g) ? "lit" : "shut"), base: 378 },
    { id: "lantern", states: { shut: art + "lantern.png", lit: art + "lantern-lit.png" }, state: (g) => (lit(g) ? "lit" : "shut"), base: 370 },
    { id: "front", states: { shut: art + "front.png", lit: art + "front-lit.png" }, state: (g) => (lit(g) ? "lit" : "shut"), plane: "front" },
    { id: "near", src: art + "near.png", plane: "front" },
  ],

  // THINGS THAT MOVE BY NATURE (layout.json fx): the hum's own shimmer (a small door barely open: a portal, its rings in the
  // paint; open once it has been seen); the door in time (the portal the mirror's light opens: shut until then); the mirror's
  // light (ENGINE-20's `mirror`); the herons going past the west window, kept to its opening, and the dust in the sun, both
  // once it is open.
  fx: [
    { id: "hum", type: "portal", at: HUM, r: 16, wide: WIDE, keep: [607, 660], base: 380.5, pale: "#fff4d8", strength: 0.9, bend: 0.8, under: ["lit"] },
    { id: "door", type: "portal", at: HUM, r: 63, wide: WIDE, keep: [607, 660], base: 381, pale: "#fff4d8", under: ["lit", "eastshutter"] },
    // (brighter and less dimmed as it grows than the engine's defaults: it lands on a wall the sun has lit already)
    { id: "light", type: "mirror", target: HUM, holder: "mom", hand: [18, 100], sizes: SIZES, flat: 1 / WIDE, fit: "height", image: "cross", shown: false,
      door: "door", doorK: 0, on: 0, color: "#fffaf0", opacity: 1, dim: 0.3, reach: [50, 268, 610, 82], base: 381.5, when: lit },
    { id: "herons", type: "birds", lanes: [[[-40, 250], [220, 236]], [[200, 262], [-40, 272]]], every: [18, 40], group: [1, 2], speed: 55, scale: 0.9,
      clip: [[[129, 331], [-22, 364], [-22, 153], [129, 195]]], frames: { foot: [28, 24], face: "E", glide: ["heron-fly-1.png"], flap: ["heron-fly-2.png", "heron-fly-3.png"] }, plane: "back", when: lit },
    { id: "dust", type: "shimmer", poly: [[180, 240], [620, 240], [800, 520], [0, 520]], count: 24, size: 2, flow: [1, 0], life: 3.0, color: "#f6eed8", opacity: 0.25, when: lit },
  ],

  // The warden at the top of the stairs with the pink light in both hands (PEOPLE-20: `shinnosuke`; he kneels, he stands).
  actors: [
    { id: "shinnosuke", kind: "shinnosuke", at: M.shinnosuke, face: "W", life: { fidget: [4, 9], still: true } },
  ],

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    // While Mom holds the light: the floor behind her is where she backs to, a step at a time (the whole floor, under everything)
    { id: "backaway", name: "floor", verb: "Back away across", poly: FLOOR, face: "E", when: momHolds, look: each("edo.top.floor"), use: (g) => backAway(g, false) },
    thing("rafters", "rafters", { poly: [[200, 204], [600, 204], [799, 0], [0, 0]] }, M.mid, "N"),
    { id: "northshutter", name: "north shutters", poly: [[347, 315], [453, 315], [453, 231], [347, 231]], walkTo: M.north, face: "N", look: SIDE_LOOK("north"), use: SIDE_USE("north") },
    { id: "eastshutter", name: "east shutters", poly: [[671, 331], [799, 359], [799, 158], [671, 195]], walkTo: M.east, face: "E", look: SIDE_LOOK("east"), use: SIDE_USE("east") },
    // the west bay: shutters, barred; open, the window (its leaves folded back against the wall at its side), and in it the view
    // below and the herons going past above
    { id: "westshutter", name: "west shutters", poly: westBay, walkTo: M.west, face: "W", when: (g) => !lit(g), look: SIDE_LOOK("west"), use: SIDE_USE("west") },
    { id: "westwindow", name: "west window", poly: westOpen, walkTo: M.west, face: "W", when: (g) => lit(g) && !momHolds(g), look: SIDE_LOOK("west"), use: SIDE_USE("west") },
    { id: "westwindow-back", name: "west window", verb: "Back away to", poly: westOpen, face: "E", when: momHolds, look: SIDE_LOOK("west"), use: SIDE_USE("west") },
    thing("view", "view", { poly: [[129, 262], [129, 331], [0, 359], [0, 272]] }, M.west, "W", { when: lit }),
    thing("herons", "herons", { poly: [[129, 195], [129, 262], [0, 272], [0, 158]] }, M.west, "W", { when: lit }),
    { id: "southshutter", name: "south shutters", poly: [[0, 584], [799, 584], [799, 599], [0, 599]], walkTo: M.south, face: "S", look: SIDE_LOOK("south"), use: SIDE_USE("south") },
    // the floor in front, where nobody walks (the walk ends at row 470)
    thing("floor", "floor", { poly: [[186, 474], [630, 474], [630, 584], [96, 584]] }, M.mid, "S"),
    thing("lantern", "old lantern", { poly: [[344, 325], [366, 325], [366, 370], [344, 370]] }, M.north, "W"),
    // the hum, in the east wall: a shimmer in the air (nothing painted); the door, once the light is on it
    ...[["hum", "place that hums", (g) => !is(g, "edo.letterbox")], ["door", "door in the light", (g) => is(g, "edo.letterbox")]].map(([id, name, when]) => ({ id, name, poly: HUM_POLY, walkTo: M.hum, face: "E", when,
      look: humLook, use: humUse, useWith: { mirror: humMirror, coin: each("edo.top.hum.with.coin"), lilflash: each("edo.top.hum.with.lilflash") } })),
    // the warden at the top of the stairs
    { id: "shinnosuke", name: "Shinnosuke", verb: "Talk to", rect: [256, 298, 46, 156], walkTo: TO_WARDEN, face: "W", when: (g) => !is(g, "edo.door"),
      look: each("edo.top.shinnosuke"), use: wardenUse },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and as the stage is built.
  setup(g) {
    for (const id of ["bigsis", "lilsis"]) if (g.dressOf(id) !== "edo-crew") g.dress(id, "edo-crew");
    const wear = momUp(g) ? "edo-crew-mirror" : "edo-crew";
    if (g.dressOf("mom") !== wear) g.dress("mom", wear);
    const sh = warden(g);
    if (sh) {
      if (is(g, "edo.door")) { sh.place(MOUTH[0], MOUTH[1], sh.scale); sh.face("E"); sh.hold(true, "mirror"); }
      else if (is(g, "edo.knelt") && !is(g, "edo.truth")) sh.kneel(true);
      else { sh.face(lit(g) ? "E" : "W"); sh.hold(true, "light"); }
    }
    const light = g.effects.get("light"), on = is(g, "edo.letterbox") ? 1 : 0;
    if (light) light.set({ holder: is(g, "edo.door") ? "shinnosuke" : "mom", on, doorK: on, shown: is(g, "edo.doorway") });
    shimmer(g);
    room.hum = null;
  },

  async enter(g) {
    if (!is(g, "edo.knelt")) return arrive(g);
    if (is(g, "edo.door") && !is(g, "edo.done")) return theStep(g);
  },

  given(g, item, to, from) {
    if (item === "coin" && to === "mom") return coinToMom(g, from);
  },
};

export const PLACES = { M, WAY_BACK, TO_WARDEN, BESIDE_MOM, MOM_OUT, MOUTH, ASIDE, HUM, SIZES };
export { TOP as topTalk, DOOR as doorTalk, GROWING, backAway };

// Act Six, the second leg: the room under the storehouse (SCENES-20B: new in round twenty, replacing ENGINE-20's stub;
// briefs/SCENES-20.md, and the design, briefs/out/edo-design.md, #26 and #27). A low room dug into the hill, timber-propped,
// earthen walls, straw mats, three small oil lamps; a ladder up to the trapdoor; at the end a closet altar, and the
// grandmother's bronze mirror on its stand. The game's invention, in the spirit of the hidden rooms that were real.
//
//   #26 Our Father        three strangers come down the ladder (edo-storehouse.js): Grandmother Sei, Jinsuke with his arms out
//                         in front of his daughter, O-Rin behind him. "We are charcoal-burners." (the talk's first node, then
//                         the room to look at); then the talk (talk/edo-b.js roomTree): nobody lies, nobody can say the true
//                         thing first; Little Sister prays out loud; "Ten ni mashimasu..."; the doors; the verse; O-Rin
//                         laughs once; the night (edo.trusted).
//   the night             the three of them talk with Sei, Jinsuke and O-Rin (their trees: the mirror, the trowel's cousin,
//                         the light with no fire), and sleep on the mats; Little Sister leaves her flashlight on for O-Rin.
//   #27 (below)           the morning: O-Rin's warning (edo.watch); Mom stays below with Sei (edo.momBelow); the flashlight on
//                         the mats, pink up between the boards: "Sorry, light." (edo.pinkOff). The constable is the
//                         storehouse's (edo-storehouse.js). When he has gone: the sun down the ladder, and the grandmother's
//                         mirror (talk/edo-b.js mirrorTree: the cross in its light on the wall, ENGINE-20's `mirror` kind; the
//                         gift; Jinsuke's trowel; the castle's two stories; edo.mirror). Mom holds it up in the sun until
//                         she moves; then up the ladder, and "Three days later" (cutscenes/edo-walk.js).
//
// Every place is PAINT-20F's own measurement of the finished picture (art/scenes/edo-chapel/layout.json and its ready.md);
// where a place was set by eye the comment says so.
//
// Try it: index.html?scene=edo-chapel&lead=mom&flags=edo.sailed,edo.boated,edo.unbarred,edo.matMoved,edo.knocked,edo.hidden   (SCENES-21B: and edo.boated)

import { STOCK_DRESSED, is } from "./edo-common.js";
import { THREE, who, heard, evening, night, morning, sunUp, hats, TALK, keepBelow, passing, partyOf, sceneOf, afterStep, talkToIsuke,
  giveTo, takeFrom, carries, pinkOn, MATES } from "./edo-hills.js";
import { roomTree, seiTree, jinsukeTree, orinTree, mirrorTree } from "../talk/edo-b.js";
import { url } from "../../engine/assets.js";

const art = "art/scenes/edo-chapel/";

// ---------- the room (layout.json: horizon 243, full 362; a grown-up 143 px at the back wall, 195 at the walk's front) ----------
const WALK = [[205, 352], [361, 350], [359, 361], [472, 359], [467, 353], [508, 352], [503, 348], [571, 347], [640, 384], [142, 392]];
const BLOCKED = [[[364, 355], [380, 355], [380, 359], [364, 359]]];
const M = { ladder: [326, 388], altar: [428, 364], sei: [501, 361], jinsuke: [578, 375], orin: [591, 363], sit: [357, 373], sit1: [306, 376], sit2: [358, 371],
  sit3: [408, 376], sunpatch: [333, 380], atwall: [303, 360], atmirror: [492, 358], atlamp: [167, 383], front: [473, 384] };
/** The bare earth wall where the grandmother turns the mirror's light: the patch's middle (layout.json lights.wall). */
const WALL = [312, 263];
/** The flashlight on the mats, left on for O-Rin (set by eye: by Little Sister's place, under the hatch, pointing up). */
const FLASH = [232, 388];
/** Where Little Sister kneels down to it (set by eye: at its left, clear of the ladder's foot). */
const AT_FLASH = [207, 390];
/** The mirror's moment (set by eye, so that nobody stands between the mirror and the wall): the grandmother in the sun at the
    right of the patch on the mats, turned to the wall; the family a step to the right; Mom, with the mirror, where she stood. */
const SEI_SUN = [356, 382];
const MOM_SUN = [358, 382];
const STAND = { mom: [398, 380], bigsis: [436, 383], lilsis: [468, 386] };
/** Asleep on the mats, the night of #26 (the layout's sit marks), and Mom with the grandmother in the morning (set by eye). */
const SLEEP = { lilsis: [306, 378], mom: [358, 372], bigsis: [410, 377] };
const BY_SEI = [464, 371];
/** Where Little Sister says her prayers, if she was standing behind the ladder (set by eye). */
const PRAY_AT = [334, 390];
/** The mats' front edge, in front of where people stand (the walk is the mats themselves: a click there walks). */
const MATS = [[142, 394], [640, 386], [700, 419], [86, 431]];

// ---------- the states of the cut-outs, from the story ----------
/** The hatch overhead: shut (with the storehouse lantern's line at its edge) before they come down and while the sacks are on
    it; open on the storehouse (lamp) from the first time down; open on the morning sun once the constable has gone (day). */
const hatch = (g) => (sunUp(g) ? "day" : is(g, "edo.hidden") && !is(g, "edo.sacksHid") ? "lamp" : "shut");
/** The mirror on its stand: until the grandmother takes it down into the sun, and it is Mom's. */
const onStand = (g) => !is(g, "edo.crossShown") && !g.holder("mirror");
/** The cross in the light on the wall: in the grandmother's hands, or in Mom's after (the light as she holds it up). */
const crossLit = (g) => is(g, "edo.crossShown") || is(g, "edo.mirrorUp");

// ---------- #26: the room's talk, and its staging (talk/edo-b.js roomTree's hooks) ----------
/** Little Sister folds her hands, wherever she is standing, and says it out loud; the others stand still. */
async function pray(g) {
  const l = g.actor("lilsis");
  if (!l) return;
  if (l.x < 300) await g.walkTo(PRAY_AT[0], PRAY_AT[1], "lilsis");          // (out from behind the ladder, where everyone can see her)
  l.face("NE"); l.pray(true);
}
/** "Jinsuke. The doors." The grandmother gets up and opens the closet altar herself, and stands by it. */
async function openAltar(g) {
  const l = g.actor("lilsis"), s = g.actor("sei");
  if (l) l.pray(false);
  if (s) {
    await s.sit(false, g.clock);
    await g.walkTo(M.altar[0] + 6, M.altar[1] + 2, "sei");
    s.face("N");
    s.hold(true, "doors");
    await g.wait(450);
  }
  g.sfx("shutter");
  g.flag("edo.altarOpen", true);
  g.follow();
  await g.wait(600);
  if (s) { s.hold(false); s.face("SW"); }
}
/** O-Rin laughs out loud, once, and covers her mouth. */
async function laugh(g) {
  const o = g.actor("orin");
  if (o) await o.fidget("laugh");
}
/** The night: the grandmother back on her mat by her mirror, Jinsuke kneeling, the family on the mats. */
async function settle(g) {
  const s = g.actor("sei"), j = g.actor("jinsuke");
  if (s && !s.seated) { await g.walkTo(M.sei[0], M.sei[1] + 6, "sei"); s.face("S"); await s.sit(true, g.clock); }
  await Promise.all(THREE.map(async (id) => { if (g.actor(id)) await g.walkTo(SLEEP[id][0], SLEEP[id][1] + 4, id); }));
  for (const id of THREE) { const f = g.actor(id); if (f) f.face("S"); }
  if (j) j.kneel("back");                                                      // (the family stays on its feet: they walk about tonight)
}
const RAW_ROOM = roomTree({ pray, openAltar, laugh, settle });
/** The room's talk as WRITE-20B wrote it, but its first node (the meeting at the ladder's foot) ends it: the room is then the
    player's to look at (the shut cupboard, O-Rin's folded hands), and a word with any of the three goes on from there. */
const ROOM = { ...RAW_ROOM, nodes: { ...RAW_ROOM.nodes, meet: { ...RAW_ROOM.nodes.meet, then: (g) => { g.flag("edo.roomMet", true); return "exit"; } } } };

/** Down the ladder the first time: Jinsuke with his arms out in front of his daughter, O-Rin peeking round him. */
async function meet(g) {
  const j = g.actor("jinsuke"), o = g.actor("orin");
  if (j) { j.face("W"); j.hold(true, "shield"); }
  if (o) { o.face("W"); o.hold(true, "peek"); }
  for (const id of THREE) { const f = g.actor(id); if (f) f.face("E"); }      // (the family turned to them)
  await g.wait(600);
  await g.talk(ROOM);
  if (j) j.hold(false);
  if (o) o.hold(false);
}

// ---------- the night: their own trees ----------
/** O-Rin presses the end of the pink flashlight, and it comes on in her hands (a glow at her hands for a moment). */
async function showLight(g) {
  const o = g.actor("orin"), live = g.view.liveEl;
  if (!o || !live) return;
  const x = o.x - 8, y = o.y - o.h * o.scale * 0.45, SVG = "http://www.w3.org/2000/svg", glow = document.createElementNS(SVG, "circle");
  glow.setAttribute("cx", x); glow.setAttribute("cy", y); glow.setAttribute("r", 46); glow.setAttribute("fill", "url(#edo-pinkglow)"); glow.setAttribute("opacity", "0");
  live.appendChild(glow);
  try { await g.tween(250, (k) => glow.setAttribute("opacity", k)); await g.wait(1600); await g.tween(400, (k) => glow.setAttribute("opacity", 1 - k)); }
  finally { glow.remove(); }
}
const SEI = seiTree({});
const JINSUKE = jinsukeTree({});
const ORIN = orinTree({ showLight });

// ---------- the night: sleep, and the morning's warning ----------
/** The mats at night: they sleep. Little Sister leaves her flashlight on for O-Rin, on the mats by her, pointing up; O-Rin goes
    up at first light to watch the path, and comes down the ladder white: a man on the path (edo.watch). */
async function sleep(g) {
  await g.fade(1, 900);
  for (const id of THREE) if (sceneOf(g, id) !== "edo-chapel" && id !== who(g)) await g.putLead(id, "edo-chapel", SLEEP[id]);
  for (const id of THREE) { const f = g.actor(id); if (f) { if (f.kneel) f.kneel(false); f.place(SLEEP[id][0], SLEEP[id][1], g.sizeAt(SLEEP[id][0], SLEEP[id][1])).face("S"); g.rememberPlace(id); } }
  const holder = THREE.find((id) => carries(g, id, "lilflash"));
  if (holder) { takeFrom(g, holder, "lilflash"); g.flag("edo.lightLeft", true); } else g.flag("edo.pinkOff", true);
  g.dress("lilsis", "edo-lying");
  const l = g.actor("lilsis");
  if (l) l.face("E");
  const m = g.actor("mom");
  if (m) m.kneel("back");
  g.view.cast.remove("orin");
  showFlash(g);
  g.follow();
  await g.wait(1800);
  await g.fade(0, 1100);
  // morning: O-Rin comes down the ladder
  const o = g.view.cast.addFigure("orin", "orin", M.ladder[0] - 22, M.ladder[1] + 2, g.sizeAt(M.ladder[0] - 22, M.ladder[1] + 2)).face("E");
  o.fade(0);
  await g.view.cast.load();
  await Promise.all([g.tween(350, (k) => o.fade(k)), g.walkTo(M.jinsuke[0] - 40, M.jinsuke[1] - 2, "orin")]);
  o.face("E");
  const j = g.actor("jinsuke");
  if (j) j.kneel(false);
  await g.say("edo.chapel.watch.1", "edo.chapel.watch.2", "edo.chapel.watch.3", "edo.chapel.watch.3b");
  g.dress("lilsis", "edo-hatback");
  if (m) m.kneel(false);
  await g.say("edo.chapel.watch.4", "edo.chapel.watch.5", "edo.chapel.watch.6", "edo.chapel.watch.7");
  g.flag("edo.watch", true);
  keepBelow(g);
  // Jinsuke and O-Rin go up to the storehouse; Mom goes to sit with the grandmother
  await Promise.all([j ? g.walkTo(M.ladder[0] - 10, M.ladder[1] + 2, "jinsuke") : null, g.walkTo(M.ladder[0] + 6, M.ladder[1], "orin"),
    who(g) !== "mom" && m ? g.walkTo(BY_SEI[0], BY_SEI[1], "mom") : null]);
  await Promise.all(["jinsuke", "orin"].map((id) => { const f = g.actor(id); return f ? g.tween(350, (k) => f.fade(1 - k)) : null; }));
  g.view.cast.remove("jinsuke"); g.view.cast.remove("orin");
  if (who(g) !== "mom" && m) m.face("E");
  const s = g.actor("sei");
  if (s) s.pray(true);
  g.follow();
  g.tidy();
}

// ---------- #27 below: the flashlight on the mats ----------
/** Her flashlight on the mats, on, pointing up (its picture, and its pink glow on the live layer). */
function showFlash(g) {
  if (!g.view.cast.get("lilflash-mats")) {
    const k = 0.34 * g.sizeAt(FLASH[0], FLASH[1]);
    g.view.cast.addPicture("lilflash-mats", { src: "art/items/lilflash.png", foot: [32, 52] }, FLASH[0], FLASH[1], k);
  }
  const el = g.q("#edo-flashglow");
  if (el) el.setAttribute("opacity", "1");
}
function hideFlash(g) {
  g.view.cast.remove("lilflash-mats");
  const el = g.q("#edo-flashglow");
  if (el) el.setAttribute("opacity", "0");
}
/** Little Sister turns it off ("Sorry, light.") and has it back in her pockets; Mom and Big Sister leave it to her. */
async function lightOff(g) {
  const me = who(g);
  if (me !== "lilsis") return g.say(`edo.chapel.lilflash.use.${me}`);
  if (g.lead && Math.hypot(g.lead.x - AT_FLASH[0], g.lead.y - AT_FLASH[1]) > 12) await g.walkTo(AT_FLASH[0], AT_FLASH[1]);
  if (g.lead) g.lead.face("E");
  await g.reach(true);
  hideFlash(g);
  await g.say("edo.chapel.lilflash.use.lilsis");
  g.flag("edo.pinkOff", true);
  giveTo(g, "lilsis", "lilflash");
  g.follow();
  await afterStep(g);
}

// ---------- the ladder ----------
/** Up the ladder. While the room's talk is not finished (the evening), and when the grandmother has something for Mom (after
    the constable), not yet: the girls want to, and Mom says in a moment. In the morning Mom, once he is at the door, does not
    go up (if he asks her, she will tell him); through the sacks over the trapdoor (O-Rin shifts them). After the mirror: on
    to Himeji. */
async function ladder(g) {
  const me = who(g);
  if (evening(g) || (sunUp(g) && !is(g, "edo.mirror"))) {
    if (me !== "mom") await g.say(`edo.chapel.ladder.use.${me}`);
    return g.say("edo.chapel.ladder.use.mom");
  }
  if (is(g, "edo.mirror")) return g.cutscene("edo-walk");
  if (me === "mom" && morning(g) && is(g, "edo.isukeAtDoor")) return g.say("edo.store.isuke.use.mom");
  if (me !== "mom" && !heard(g, `edo.chapel.ladder.use.${me}`)) await g.say(`edo.chapel.ladder.use.${me}`);
  g.sfx("trapdoor");
  if (morning(g) && is(g, "edo.sacksHid")) { await g.fade(1, 300); passing.by = "pile"; return g.goto("edo-storehouse", { spawn: "trapdoor", via: "cut" }); }
  return g.goto("edo-storehouse", { spawn: "trapdoor" });
}

// ---------- the people ----------
/** What each of them says to the grandmother in the morning, kneeling with her: the plan, as the warning made it. */
const PLAN = { mom: "edo.chapel.watch.4", bigsis: "edo.chapel.watch.5", lilsis: "edo.chapel.watch.6" };
function sei(g) {
  if (!is(g, "edo.trusted")) return g.talk(ROOM);
  if (morning(g)) return g.say(PLAN[who(g)]);
  if (sunUp(g) && !is(g, "edo.mirror")) return mirrorMoment(g);
  if (is(g, "edo.mirror")) return g.say(`edo.chapel.sei.${who(g)}`);
  return g.talk(SEI);
}
function jinsuke(g) {
  if (!is(g, "edo.trusted")) return g.talk(ROOM);
  if (is(g, "edo.mirror")) return g.say(`edo.chapel.jinsuke.${who(g)}`);
  return g.talk(JINSUKE);
}
function orin(g) {
  if (!is(g, "edo.trusted")) return g.talk(ROOM);
  if (night(g)) return g.talk(ORIN);
  return g.say(`edo.chapel.orin.${who(g)}`);
}

// ---------- #27's end: the mirror (talk/edo-b.js mirrorTree's hooks) ----------
/** She takes the mirror down off its stand, stands in the sun from the open trapdoor, and turns its light onto the earth wall:
    in the patch, a cross that is nowhere on the mirror (ENGINE-20's `mirror` kind: the light `cross-sei`). */
async function sunOnMirror(g) {
  const s = g.actor("sei");
  if (s) {
    await s.sit(false, g.clock);
    await g.walkTo(SEI_SUN[0], SEI_SUN[1], "sei");
    s.face("NW");
    s.hold(true, "mirror");
  }
  await g.wait(300);
  g.flag("edo.crossShown", true);
  g.follow();
  await g.wait(1400);
}
/** "Then I'll carry it, and I'll find it some sun." The mirror into Mom's hands; she holds it up where the grandmother stood,
    and the light is on the wall again from hers (the light `cross-mom`); the grandmother goes back to her place. */
async function giveMirror(g) {
  const s = g.actor("sei"), m = g.actor("mom");
  if (m) await g.walkTo(SEI_SUN[0] + 30, SEI_SUN[1] + 2, "mom");
  if (s) s.hold(false);
  g.flag("edo.crossShown", false);
  g.follow();
  giveTo(g, "mom", "mirror");
  if (s) { await g.walkTo(M.sei[0], M.sei[1] + 6, "sei"); s.face("S"); await s.sit(true, g.clock); }
  g.follow();                                                                  // (the ground she stood on is free again)
  if (m) { await g.walkTo(MOM_SUN[0], MOM_SUN[1], "mom"); m.place(MOM_SUN[0], MOM_SUN[1], g.sizeAt(MOM_SUN[0], MOM_SUN[1])); g.rememberPlace("mom"); }
  await raised(g);
}
/** Jinsuke's trowel for his cousin Tomezō: into Mom's sash (her hands are full of mirror). */
async function giveTrowel(g) {
  const j = g.actor("jinsuke");
  if (j) { j.kneel(false); await g.walkTo(MOM_SUN[0] + 40, MOM_SUN[1] + 4, "jinsuke"); j.face("W"); await j.play(g.clock, "reach"); }
  giveTo(g, "mom", "trowel");
  if (j) { await g.walkTo(M.jinsuke[0], M.jinsuke[1], "jinsuke"); j.face("W"); }
}
const MIRROR = mirrorTree({ sunOnMirror, giveMirror, giveTrowel });
/** The grandmother has something for Mom: the family by the wall, and the mirror's moment, to "Then we go to Himeji." */
async function mirrorMoment(g) {
  await Promise.all(THREE.map(async (id) => { if (g.actor(id)) { await g.walkTo(STAND[id][0], STAND[id][1], id); g.actor(id).face("NW"); } }));
  await g.talk(MIRROR);
}
/** Mom holds the mirror up in the sun, facing the wall: the cross on the wall again (`edo.mirrorUp`), until she moves. */
async function raised(g) {
  const m = g.actor("mom");
  g.dress("mom", "edo-mirror");
  if (m) m.face("NW");
  g.flag("edo.mirrorUp", true);
  g.follow();
  await g.wait(400);
}
/** Mom with the mirror in the sun again (the mirror on the wall or the sun on the mats). */
async function raise(g) {
  if (who(g) !== "mom" || !g.has("mirror") || !sunUp(g)) return g.say(g.fallback("nope"));
  if (is(g, "edo.mirrorUp")) return g.say(`edo.chapel.wall.cross.${who(g)}`);
  await g.walkTo(MOM_SUN[0], MOM_SUN[1]);
  if (g.lead) { g.lead.place(MOM_SUN[0], MOM_SUN[1], g.sizeAt(MOM_SUN[0], MOM_SUN[1])); g.rememberPlace(); }
  await raised(g);
  await g.say("edo.chapel.wall.cross.mom");
}

// ---------- the scene ----------
const each = (id) => ({ mom: `${id}.mom`, bigsis: `${id}.bigsis`, lilsis: `${id}.lilsis` });
export default {
  id: "edo-chapel",
  era: "edo",
  name: "The room under the storehouse",
  music: "edo-hidden",

  horizon: 243, full: 362, maxScale: 1.25,
  walk: { area: WALK },
  blocked: BLOCKED,
  spawn: { default: M.sit, ...M },
  // down the ladder: the other two beside whoever comes first (the layout's fromLadder places, near enough)
  arrive: { ladder: [[392, 384], [434, 386]] },
  facing: "N",
  party: partyOf,
  // Mom, holding the mirror up in the sun with the cross on the wall, stays where she is (what she does, she does from there)
  still: (g, id) => id === "mom" && is(g, "edo.mirrorUp"),
  exits: ["edo-storehouse"],
  stock: STOCK_DRESSED,
  talk: TALK,

  picture: art + "back.png",
  planes: [
    { id: "trapdoor", states: { shut: art + "trapdoor-shut.png", lamp: art + "trapdoor-lamp.png", day: art + "trapdoor-day.png" }, state: hatch, plane: "back" },
    { id: "lamps", states: { lit: art + "lamps.png", out: art + "lamps-out.png" }, state: "lit", plane: "back" },
    { id: "props", src: art + "props.png", base: [[76, 413], [703, 402]], solid: [[72, 410], [92, 409], [80, 417], [60, 417]] },
    { id: "altar", states: { shut: art + "altar-shut.png", open: art + "altar-open.png" }, state: (g) => (is(g, "edo.altarOpen") ? "open" : "shut"),
      base: [[381, 354], [457, 353]], solid: [[381, 345], [451, 345], [457, 353], [381, 354]] },
    { id: "mirror", src: art + "mirror.png", base: [[473, 351], [498, 351]], when: onStand },
    { id: "ladder", states: { lamp: art + "ladder.png", day: art + "ladder-day.png" }, state: (g) => (sunUp(g) ? "day" : "lamp"),
      base: [[253, 399], [284, 398]], solid: [[250, 397], [291, 396], [288, 401], [246, 402]] },
    { id: "front", src: art + "front.png", plane: "front" },
  ],
  // The morning sun down the open trapdoor onto the mats (the painting has its patch: this is the light in the air), and her
  // flashlight's pink glow on the mats and up at the boards over it (#27, while it is on).
  live: (kit, g) => `<defs>
      <linearGradient id="edo-sunbeam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffbe6" stop-opacity="0.28"/><stop offset="1" stop-color="#fff3cf" stop-opacity="0.08"/></linearGradient>
      <radialGradient id="edo-pinkglow"><stop offset="0" stop-color="#ffc4ea" stop-opacity="1"/><stop offset="0.4" stop-color="#ff6fc4" stop-opacity="0.6"/><stop offset="1" stop-color="#ff5ab8" stop-opacity="0"/></radialGradient>
      <filter id="edo-soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter></defs>
    <polygon id="edo-sun" points="183,168 295,169 373,386 273,386" fill="url(#edo-sunbeam)" filter="url(#edo-soft)" opacity="${sunUp(g) ? 1 : 0}"/>
    <g id="edo-flashglow" opacity="${pinkOn(g) ? 1 : 0}">
      <polygon points="${FLASH[0] - 6},${FLASH[1] - 4} ${FLASH[0] + 8},${FLASH[1] - 4} ${FLASH[0] + 36},190 ${FLASH[0] - 30},190" fill="#ff9ad6" opacity="0.12" filter="url(#edo-soft)"/>
      <ellipse cx="${FLASH[0] + 2}" cy="196" rx="44" ry="10" fill="url(#edo-pinkglow)" opacity="0.6"/>
      <ellipse cx="${FLASH[0] + 2}" cy="${FLASH[1] - 2}" rx="26" ry="7" fill="url(#edo-pinkglow)"/></g>`,
  fx: [
    // the three lamps' flames (layout.json fx: they stay lit; "The lamp stays lit tonight.")
    { id: "lamp-left", type: "flame", at: [117, 266], size: 9, width: 4, glow: 26, glowColor: "#ffb060", glowOpacity: 0.26, flicker: 0.5, plane: "back" },
    { id: "lamp-stand", type: "flame", at: [372, 294], size: 9, width: 4, glow: 26, glowColor: "#ffb060", glowOpacity: 0.26, flicker: 0.5, plane: "back" },
    { id: "lamp-altar-r", type: "flame", at: [498, 250], size: 9, width: 4, glow: 26, glowColor: "#ffb060", glowOpacity: 0.26, flicker: 0.5, plane: "back" },
    // ENGINE-20's mirror light: the patch on the wall with the cross in it, from the grandmother's hands, then from Mom's
    { id: "cross-sei", type: "mirror", when: (g) => is(g, "edo.crossShown"), target: WALL, holder: "sei", hand: [8, 84], reach: [296, 230, 110, 160],
      sizes: [[36, 14.5], [200, 34]], flat: 1.05, image: "cross", shown: true, plane: "back" },
    { id: "cross-mom", type: "mirror", when: (g) => is(g, "edo.mirrorUp"), target: WALL, holder: "mom", hand: [10, 104], reach: [296, 200, 110, 190],
      sizes: [[36, 14.5], [200, 34]], flat: 1.05, image: "cross", shown: true, plane: "back" },
  ],

  // Grandmother Sei by her mirror, kneeling (seiza: PEOPLE-20's `sei` is found so); Jinsuke and O-Rin, except in the morning,
  // when they are up in the storehouse keeping the door and the watch.
  actors: [
    { id: "sei", kind: "sei", at: M.sei, face: "S", life: { fidget: [6, 12] } },
    { id: "jinsuke", kind: "jinsuke", at: M.jinsuke, face: "W", when: (g) => !morning(g), life: { fidget: [6, 12] } },
    { id: "orin", kind: "orin", at: M.orin, face: "W", when: (g) => !morning(g), life: { fidget: [4, 9] } },
  ],

  // Back to front: a later area lies over an earlier one (the other two first: edo-hills.js MATES).
  hotspots: [
    ...MATES,
    { id: "beams", name: "beams", rect: [0, 107, 800, 100], walkTo: M.sit, face: "N", look: each("edo.chapel.beams"), use: each("edo.chapel.beams.use") },
    { id: "props", name: "timber props", poly: [[146, 198], [172, 198], [172, 366], [146, 366]], walkTo: M.atlamp, face: "W", look: each("edo.chapel.props"), use: each("edo.chapel.props.use") },
    { id: "props-r", name: "timber props", poly: [[598, 198], [630, 198], [630, 362], [598, 362]], walkTo: [588, 368], face: "E", look: each("edo.chapel.props"), use: each("edo.chapel.props.use") },
    { id: "props-near", name: "timber props", poly: [[58, 186], [94, 186], [94, 416], [58, 416]], walkTo: M.atlamp, face: "W", look: each("edo.chapel.props"), use: each("edo.chapel.props.use") },
    { id: "wall", name: "earth wall", rect: [278, 228, 67, 70], walkTo: M.atwall, face: "N",
      look: (g) => g.say(crossLit(g) ? `edo.chapel.wall.cross.${who(g)}` : `edo.chapel.wall.${who(g)}`), use: each("edo.chapel.wall.use"), useWith: { mirror: raise } },
    { id: "mats", name: "straw mats", poly: MATS, walkTo: M.sit, face: "N", when: (g) => !night(g),
      look: each("edo.chapel.mats"), use: (g) => g.say(`edo.chapel.mats.use.${who(g)}`) },
    { id: "mats-night", name: "straw mats", poly: MATS, walkTo: M.sit, face: "N", when: night, verb: "Sleep on", look: each("edo.chapel.mats"), use: sleep },
    { id: "trapdoor", name: "trapdoor", rect: [99, 144, 210, 33], walkTo: M.ladder, face: "W", when: (g) => is(g, "edo.watch"),
      look: each("edo.chapel.trapdoor"), use: each("edo.chapel.trapdoor.use") },
    { id: "ladder", name: "ladder", rect: [212, 151, 76, 250], walkTo: M.ladder, face: "W", look: each("edo.chapel.ladder"), use: ladder, verb: "Climb" },
    { id: "lamp-left", name: "oil lamp", rect: [105, 261, 27, 15], walkTo: M.atlamp, face: "W", look: each("edo.chapel.lamps"), use: each("edo.chapel.lamps.use") },
    { id: "altar", name: "closet altar", rect: [381, 258, 77, 97], walkTo: M.altar, face: "N", when: (g) => !is(g, "edo.altarOpen"),
      look: each("edo.chapel.altar"), use: each("edo.chapel.altar.use") },
    { id: "altar-open", name: "closet altar", rect: [370, 258, 105, 97], walkTo: M.altar, face: "N", when: (g) => is(g, "edo.altarOpen"),
      look: each("edo.chapel.altar.open"), use: each("edo.chapel.altar.open.use") },
    { id: "kannon", name: "white Kannon", rect: [409, 279, 17, 36], walkTo: M.altar, face: "N", when: (g) => is(g, "edo.altarOpen"),
      look: each("edo.chapel.kannon"), use: each("edo.chapel.kannon.use") },
    { id: "calendar", name: "folded paper", rect: [391, 292, 18, 22], walkTo: M.altar, face: "N", when: (g) => is(g, "edo.altarOpen"),
      look: each("edo.chapel.calendar"), use: each("edo.chapel.calendar.use") },
    { id: "bowl", name: "bowl of water", rect: [430, 304, 16, 11], walkTo: M.altar, face: "N", when: (g) => is(g, "edo.altarOpen"),
      look: each("edo.chapel.bowl"), use: each("edo.chapel.bowl.use") },
    { id: "lampstand", name: "oil lamp", rect: [362, 291, 19, 68], walkTo: M.altar, face: "NW", look: each("edo.chapel.lamps"), use: each("edo.chapel.lamps.use") },
    { id: "lamp-altar-r", name: "oil lamp", rect: [489, 246, 17, 12], walkTo: M.atmirror, face: "N", look: each("edo.chapel.lamps"), use: each("edo.chapel.lamps.use") },
    { id: "stand", name: "mirror stand", rect: [469, 302, 30, 49], walkTo: M.atmirror, face: "N", look: each("edo.chapel.stand"), use: each("edo.chapel.stand.use") },
    { id: "mirror", name: "bronze mirror", rect: [473, 295, 20, 19], walkTo: M.atmirror, face: "N", when: onStand,
      look: each("edo.chapel.mirror"), use: each("edo.chapel.mirror.use") },
    { id: "basket", name: "basket", rect: [52, 378, 91, 85], walkTo: M.atlamp, face: "SW", look: each("edo.chapel.basket"), use: each("edo.chapel.basket.use") },
    { id: "jar", name: "water jar", rect: [645, 357, 56, 80], walkTo: [612, 378], face: "E", look: each("edo.chapel.jar"), use: each("edo.chapel.jar.use") },
    { id: "sack", name: "charcoal sack", rect: [522, 483, 136, 105], walkTo: M.front, face: "S", look: each("edo.chapel.sack"), use: each("edo.chapel.sack.use") },
    { id: "sunpatch", name: "square of sun", rect: [273, 372, 100, 29], walkTo: M.sunpatch, face: "N", when: sunUp,
      look: each("edo.chapel.sunpatch"), use: each("edo.chapel.sunpatch.use"), useWith: { mirror: raise } },
    { id: "lilflash", name: "pink flashlight", rect: [FLASH[0] - 17, FLASH[1] - 16, 34, 20], walkTo: AT_FLASH, face: "E", when: pinkOn,
      look: each("edo.chapel.lilflash"), use: lightOff, verb: "Turn off" },
    // the constable's man above, at the door or in the room (#27): Mom hears him through the floor, and does not answer
    { id: "isuke", name: "the man upstairs", rect: [99, 107, 300, 70], walkTo: BY_SEI, face: "N",
      when: (g) => who(g) === "mom" && is(g, "edo.isukeAtDoor") && !is(g, "edo.constableGone"),
      look: (g) => g.say("edo.store.isuke.mom"), use: talkToIsuke, verb: "Listen to" },
    // the people
    { id: "sei", name: "Grandmother Sei", rect: [478, 268, 46, 96], walkTo: [470, 368], face: "E", look: each("edo.chapel.sei"), use: sei, verb: "Talk to" },
    { id: "jinsuke", name: "Jinsuke", rect: [551, 217, 54, 158], walkTo: [540, 372], face: "E", when: (g) => !morning(g),
      look: each("edo.chapel.jinsuke"), use: jinsuke, verb: "Talk to" },
    { id: "orin", name: "O-Rin", rect: [573, 256, 37, 107], walkTo: [556, 366], face: "E", when: (g) => !morning(g),
      look: each("edo.chapel.orin"), use: orin, verb: "Talk to" },
  ],

  setup(g) {
    hats(g, false);                                                            // (indoors: the hats on their backs)
    keepBelow(g);
    if (pinkOn(g)) showFlash(g);
    const s = g.actor("sei");
    if (s && morning(g)) s.pray(true);                                         // (the morning: she prays, very low, while he climbs)
    const m = g.actor("mom");
    if (m && is(g, "edo.mirrorUp")) { m.place(MOM_SUN[0], MOM_SUN[1], g.sizeAt(MOM_SUN[0], MOM_SUN[1])); m.face("NW"); }
    else if (m && morning(g) && who(g) !== "mom" && Math.hypot(m.x - BY_SEI[0], m.y - BY_SEI[1]) < 4) m.face("E");
  },

  // Mom holds the mirror up in the sun (she stays there: `still`); if something walks her off, she lowers it, and the cross goes.
  tick(g) {
    if (!is(g, "edo.mirrorUp")) return;
    const m = g.actor("mom");
    if (m && m.walking) { g.flag("edo.mirrorUp", false); g.dress("mom", "edo-hatback"); g.follow(); }
  },

  async enter(g, from) {
    const way = passing.by;
    passing.by = null;
    // #26: the first time down the ladder
    if (is(g, "edo.hidden") && !is(g, "edo.roomMet")) return meet(g);
    if (way === "pile" || way === "pinkPile") await g.say("edo.store.pile.orin");      // (up there, the sacks put back)
    // #27: Little Sister down to her flashlight, from the pink floorboards
    if ((way === "pink" || way === "pinkPile") && pinkOn(g)) return lightOff(g);
    // #27: Mom back below (the last of the three things, perhaps: he climbs to the door)
    if (morning(g) && who(g) === "mom" && from === "edo-storehouse") return afterStep(g, false);
  },
};

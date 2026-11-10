// Act Six, the fifth leg: inside the women's hall at the foot of Mount Shosha, at sunset (SCENES-21C: new in round twenty-one, in
// place of ENGINE-21's stub; briefs/SCENES-21.md, and the design, briefs/out/edo2-design.md, "INSIDE THE WOMEN'S HALL" and #38).
// A small dim hall of dark boards, slips pasted on every post and beam; the west lattice at the left with the sunset in its
// gaps; the small closed cabinet at the back (Kannon-sama inside, not shown), a cold lamp, an incense burner, flowers; the east
// wall at the right, plain plaster, where the bars of red light climb as the sun goes down, and in them, a hand's height up, the
// hum. O-Ume kneels by the way out; Ryōkai's face is at the lattice, outside, not coming in.
//
// The three come in by the open doors (edo-shosha.js), at the mark `door` (the bottom edge: the doors are behind the lens).
//
//   coming in   once: O-Ume ("He comes when the light reaches the wall."); Grandmother Tome goes home to her supper
//   the light   PAINT-21F's three light pictures on the live layer, screen-blended and clipped, moved by one number, k: 0 as they
//               come in, rising slowly; at the hum's k (0.563) the bar is on the hum, its shimmer opens, then the small door, a
//               coin wide (the `door` portal at 0.47), and the Son's voice comes through it
//   #38 A Small Door At Sunset
//     the voice   sonTree (talk/edo-d.js), held plainly (its menus are the family's; his lines go through the door with his
//                 portrait, `sonVoice`): Mom made the one being played, and she sits down before the door (the hook `sit`);
//                 "...MOM?" (edo.sonHeard). The door used again, by any of the three, is the talk again (the girls the first
//                 time say why they are not going in themselves)
//     more light  Little Sister's flashlight on the door (or the hum): it grows to a hand (HALL.flash: edo.doorWide); she keeps
//                 it on the door, a pink light, from her place by the wall
//     supper      Mom's rice ball on the door a hand wide: on her knees, her arm in (`feed`); g.send("riceball", { to: "son" });
//                 "It's the best thing I've ever eaten." (HALL.riceball: edo.sonFed); a coin wide, "It won't fit."
//     hold hands  the talk again: tomorrow, a door at the top of a castle; "Mom. Dad went through alone. Don't." (edo.holdHands)
//     the sun goes   the hook `fade`: the bars climb to the top and fade, the flashlight flickers, the dusk; Isaiah 49:15; the
//                 hook `close`: the door shrinks to a coin, to a point, gone; O-Ume's question and Mom's answer; then the
//                 cut-scene "Mind The Fire" (cutscenes/edo-night.js)
//   wrong tries   the cabinet (HALL.kannon, the first time), Ryōkai at the lattice, the mirror on the door, into the door
//   the doorway   not before the sun has gone (doorway.use)
//
// Staging (PAINT-21F's rule): nobody stands by the east wall north of the line from the lens to the hum; Mom sits at `humsit`,
// Little Sister shines from `lil`, Big Sister watches from `big`.
//
// Every place is the painter's measurement (art/scenes/edo-hall/layout.json, PAINT-21F's ready.md), or set by eye against the
// picture with the people in it; where the two differ the comment says why.
//
// Try it: index.html?scene=edo-hall&lead=mom&flags=edo.hallOpen,edo.umeIn

import { STOCK_DRESSED } from "./edo-common.js";
import { THREE, who, is, heard, each, dressAll, thingOf, idle, TALK } from "./edo-west.js";
import { hallUmeTree, hallRyokaiTree, sonTree, sonVoice, HALL, SHOSHA_MAP } from "../talk/edo-d.js";

const art = "art/scenes/edo-hall/";

// ---------- the camera and the floor (layout.json: room.View, horizon 200, full 410) ----------
const HORIZON = 200, FULL = 410;
const FLOOR = [[163, 356], [313, 353], [308, 365], [414, 362], [411, 350], [553, 346], [694, 460], [561, 454], [0, 480]];

// ---------- the marks (layout.json marks) ----------
const M = { door: [372, 459], ume: [170, 458], mats: [344, 413], cabinet: [361, 375], lattice: [138, 400], hum: [689, 457], humsit: [612, 411],
  big: [537, 452], lil: [676, 458], mid: [403, 435] };
const RYOKAI = [50, 398];               // his feet, outside the west wall (layout.json marks.ryokai): his face at the lattice
const TOME = [252, 470], TOME_OUT = [236, 640];     // Grandmother Tome inside the door as they come in, and her way out (set by eye)

// ---------- the light (layout.json bars, hum, door) ----------
const HUM = [652, 316];
const HUM_POLY = [[663, 316], [661, 324], [657, 330], [652, 332], [646, 330], [642, 324], [640, 316], [642, 308], [646, 302], [652, 300], [657, 302], [661, 308]];
const K_HUM = 0.563, K_FLOOR = 0.372, RISE = 82.9;
const COIN = 0.47;                      // the small door a coin wide (r 9 of its 19)
const RISE_S = 26;                      // seconds the bars take to climb from the floor to the hum (the scene's choice)
// where each stage of the talk leaves the sun (k), so that a game loaded in it has the light where it was
const kOf = (g) => (is(g, "edo.sonFed") ? 0.78 : is(g, "edo.doorWide") ? 0.68 : is(g, "edo.sonHeard") ? 0.6 : 0);
const room = { k: 0, gone: 0, drawn: -1, voice: false, night: false, hum: null, humAt: null, doorAt: null };

const dusk = (g) => is(g, "edo.holdHands") || room.gone > 0.99;
/** The three light pictures where k and the sun's going (`gone`, 0 to 1) put them. */
function light(g) {
  const k = room.k, op = 1 - room.gone;
  const wall = g.q("#hall-bars-wall"), floor = g.q("#hall-bars-floor"), air = g.q("#hall-bars-air");
  if (wall) { wall.setAttribute("y", (-k * RISE).toFixed(1)); wall.parentNode.style.opacity = op.toFixed(3); }
  if (floor) {
    const f = Math.min(1, k / K_FLOOR), o = k < 0.205 ? 1 : k < K_FLOOR ? 1 - (k - 0.205) / (K_FLOOR - 0.205) : 0;
    floor.setAttribute("x", (f * 157).toFixed(1)); floor.setAttribute("y", (f * -2).toFixed(1));
    floor.parentNode.style.opacity = (o * op).toFixed(3);
  }
  if (air) air.parentNode.style.opacity = ((k < 0.8 ? 1 : Math.max(0, 1 - (k - 0.8) / 0.2)) * op).toFixed(3);
  room.drawn = k + room.gone * 10;
}
/** The hum's shimmer and the small door, as the story has them (only when that changes: a portal draws again when opened). */
function doors(g) {
  const hum = g.effects.get("hum"), door = g.effects.get("door");
  const open = is(g, "edo.sonHeard") && !dusk(g);
  const h = !open && room.k >= K_HUM && !dusk(g) ? 0.6 : 0, d = open ? (is(g, "edo.doorWide") ? 1 : COIN) : 0;
  if (hum && room.humAt !== h) { hum.open(h); room.humAt = h; }
  if (door && room.doorAt !== d) { if (d) door.open(1, { scale: d }); else door.open(0); room.doorAt = d; }
}
/** Little Sister's pink light on the door, while she shines it (a mirror-kind patch, as the keep's: from her hands to the hum). */
function pinkLight(g, on = true) {
  const old = g.effects.get("pinklight");
  if (old) old.show(false);
  if (!on) return null;
  const lil = g.actor("lilsis");
  if (!lil) return null;
  const hand = [lil.x - 6 * lil.scale, lil.y - lil.h * lil.scale * 0.58];
  return g.effects.add({ id: "pinklight", type: "mirror", target: HUM, mirror: hand, sizes: [[40, 9], [200, 16]], flat: 1.3, dim: 0, tremble: 0.6, image: null,
    color: "#ff9fd0", opacity: 0.55, on: 1, reach: [Math.min(hand[0], HUM[0]) - 12, Math.min(hand[1], HUM[1]) - 18, Math.abs(hand[0] - HUM[0]) + 24, Math.abs(hand[1] - HUM[1]) + 36], base: 415.2 });
}
const shining = (g) => is(g, "edo.doorWide") && !dusk(g);

// ---------- #38: the voice ----------
/** Mom sits down before the door (the hook `sit`: before "It's not a closet."). */
async function sit(g) {
  const mom = g.actor("mom");
  if (!mom) return;
  if (Math.hypot(mom.x - M.humsit[0], mom.y - M.humsit[1]) > 4) await g.walkTo(M.humsit[0], M.humsit[1], "mom");
  mom.face("E");
  mom.kneel("back");
  await g.wait(560);
}
/** The sun goes (the hook `fade`): the bars climb to the top of the wall and fade; the flashlight flickers; the dusk. */
async function fade(g) {
  const k0 = room.k, light0 = g.effects.get("pinklight");
  await g.tween(2600, (t) => { room.k = k0 + (1 - k0) * t; light(g); });
  if (light0) for (const on of [0.3, 1, 0.15, 0.8, 0.4]) { light0.set({ on }); await g.wait(140); }
  const dusky = Promise.all([g.fadePlane("dusk", 1, { ms: 3400 }), g.fadePlane("lattice", "dusk", { ms: 3400 }), g.fadePlane("front", "dusk", { ms: 3400 })]);
  await g.tween(3400, (t) => { room.gone = t; light(g); });
  await dusky;
}
/** The door shrinks to a coin, to a point, and is gone (the hook `close`); the light down, the hum still. */
async function close(g) {
  const door = g.effects.get("door"), lil = g.actor("lilsis");
  if (door) {
    await g.tween(900, (t) => door.open(1, { scale: 1 - (1 - COIN) * t }));
    await g.tween(800, (t) => door.open(1, { scale: COIN * (1 - t) + 0.02 * t }));
    door.open(0);
  }
  room.doorAt = 0; room.humAt = 0;
  g.sfx("portal");
  pinkLight(g, false);
  if (lil && lil.act && lil.act.low === "shine") lil.hold(false);
  g.stopLoop("hum");
  room.hum = null;
}
/** The talk is over and the sun gone (the hook `done`): the scene plays "Mind The Fire" once the talk has ended. */
function done() { room.night = true; }
const SON = sonTree({ sit, fade, close, done });
/** The talk through the door (Mom's use of it; the girls' too, each with her own branch), then the night if it is time. */
async function talkSon(g) {
  await g.talk(SON);
  if (room.night || (is(g, "edo.holdHands") && !is(g, "edo.nightDone"))) { room.night = false; await g.cutscene("edo-night"); }
}
/** The bars of light reach the hum: its shimmer, then the small door a coin wide, and the voice. The controls go to Mom. */
async function voiceComes(g) {
  room.voice = true;
  const hum = g.effects.get("hum"), door = g.effects.get("door");
  if (hum) await g.tween(900, (t) => hum.open(0.6 * t));
  if (g.loop("hum", { level: 1.2 })) room.hum = 1.2;
  await g.wait(900);
  g.sfx("portal");
  if (door) await g.tween(900, (t) => door.open(t, { scale: COIN }));
  if (hum) hum.open(0);
  room.doorAt = COIN; room.humAt = 0;
  const d = g.store.data;
  if (d.active !== "mom") {
    if (g.lead && g.lead._stop) g.lead._stop();
    d.active = "mom";
    g.store.emit();
    g.rebuildSpots();
  }
  for (const id of ["bigsis", "lilsis"]) { const a = g.actor(id); if (a) a.look(HUM[0], HUM[1]); }
  await talkSon(g);
}

// ---------- #38: the door used, and things into it ----------
/** The small door (or the hum once it is open): the talk; the girls, the first time, say why they are not going in. */
async function doorUse(g) {
  const me = who(g);
  if (me !== "mom" && !heard(g, `edo.hall.door.use.${me}`)) await g.say(`edo.hall.door.use.${me}`);
  await talkSon(g);
}
/** Little Sister's flashlight on the door: more light, more door. She stays by the wall with it, shining. */
async function flash(g) {
  const lil = g.actor("lilsis"), door = g.effects.get("door");
  if (lil && Math.hypot(lil.x - M.lil[0], lil.y - M.lil[1]) > 4) await g.walkTo(M.lil[0], M.lil[1], "lilsis");
  if (lil) { lil.look(HUM[0], HUM[1]); lil.hold(true, "shine"); }
  g.sfx("click");
  pinkLight(g, true);
  await g.say(HALL.flash[0]);
  if (door) await g.tween(1000, (t) => door.open(1, { scale: COIN + (1 - COIN) * t }));
  room.doorAt = 1;
  g.flag("edo.doorWide", true);
  await sonVoice(g, HALL.flash[1]);
}
/** Mom's rice ball into the door, a hand wide: on her knees, her arm in; it goes into the tunnel for him; he eats. */
async function feed(g) {
  const mom = g.actor("mom"), u = g.actor("ume");
  if (mom) { mom.face("E"); mom.hold(true, "feed"); }
  await g.say(HALL.riceball[0]);
  g.send("riceball", { to: "son" });
  g.sfx("portal");
  await g.wait(1400);                                        // (a long silence, then:)
  await sonVoice(g, HALL.riceball.slice(1, 4));
  if (u) u.hold(true, "laughcry");
  await g.say(HALL.riceball[4]);
  if (u) u.hold(false);
  g.flag("edo.sonFed", true);
  if (mom) { mom.hold(false); mom.kneel("back"); }
  await talkSon(g);
}
const doorWith = {
  riceball: async (g) => {
    if (who(g) !== "mom") return g.say(`edo.hall.door.with.riceball.${who(g)}`);
    if (!is(g, "edo.doorWide")) return g.say(HALL.riceballSmall);
    if (is(g, "edo.sonFed")) return g.say(g.fallback("nope"));
    return feed(g);
  },
  lilflash: async (g) => {
    if (who(g) !== "lilsis") return g.say(`edo.hall.door.with.lilflash.${who(g)}`);
    if (is(g, "edo.doorWide")) return g.say("edo.hall.door.hand.lilsis");
    return flash(g);
  },
  mirror: { mom: "edo.hall.door.with.mirror.mom" },
  coin: each("edo.hall.door.with.coin"),
  lastpenny: { lilsis: "edo.hall.door.with.lastpenny.lilsis" },
};
/** The hum before the door opens: the light isn't on it yet. */
const humWith = {
  lilflash: { lilsis: "edo.hall.hum.with.lilflash.lilsis" },
  mirror: { mom: "edo.hall.door.with.mirror.mom" },
  coin: each("edo.hall.door.with.coin"),
  lastpenny: { lilsis: "edo.hall.door.with.lastpenny.lilsis" },
  riceball: (g) => g.say(who(g) === "mom" ? HALL.riceballSmall : `edo.hall.door.with.riceball.${who(g)}`),
};
const doorLook = (g) => g.say(dusk(g) ? `edo.hall.door.shut.${who(g)}` : is(g, "edo.doorWide") ? `edo.hall.door.hand.${who(g)}` : `edo.hall.door.${who(g)}`);

// ---------- the cabinet, O-Ume, Ryōkai ----------
async function cabinetUse(g) {
  if (heard(g, HALL.kannon[0])) return g.say(`edo.hall.cabinet.use.${who(g)}`);
  const u = g.actor("ume");
  if (u && g.lead) u.look(g.lead.x, g.lead.y);
  await g.say(...HALL.kannon);
}
const UME = hallUmeTree(), RYO = hallRyokaiTree();
async function talkTo(g, id, tree) {
  const a = g.actor(id), lead = g.lead;
  if (a && lead && id !== "ryokai") a.look(lead.x, lead.y);
  await g.talk(tree);
}

// ---------- coming in ----------
async function enterHall(g) {
  await g.wait(300);
  const u = g.actor("ume"), t = g.actor("tome");
  if (u && g.lead) u.look(g.lead.x, g.lead.y);
  await g.say(HALL.enter[0]);
  if (t) { t.look(g.lead.x, g.lead.y); }
  await g.say(HALL.enter[1]);
  if (t) {
    await g.moveTo(TOME_OUT[0], TOME_OUT[1], "tome");
    t.hidden = true;
  }
  g.flag("edo.tomeHome", true);
  if (u) u.look(HUM[0], HUM[1]);
}

// ---------- the scene ----------
const thing = thingOf("hall");
const poly = (p) => ({ poly: p });
const BOX = { ume: [150, 350, 40, 108], ryokai: [36, 254, 28, 46] };

export default {
  id: "edo-hall",
  era: "edo",
  name: "Inside the women's hall",
  music: "edo-shosha",

  horizon: HORIZON, full: FULL, maxScale: 1.3,
  walk: { area: FLOOR },
  blocked: [[[321, 345], [404, 343], [408, 361], [314, 363]]],

  party: THREE,
  spawn: { default: M.door, ...M },
  arrive: { door: [[288, 463], [416, 456]] },          // (Big Sister to the left of the flowers on the altar, not in front of them)
  facing: "N",
  stock: STOCK_DRESSED,
  talk: TALK,
  travel: SHOSHA_MAP.stay,
  // Mom, sitting before the door once he has spoken, stays there; Little Sister, shining her light on it, stays by the wall
  still: (g, id) => (id === "mom" && is(g, "edo.sonHeard") && !dusk(g)) || (id === "lilsis" && shining(g)),
  tick(g, dt) {
    // the sun going down: the bars climb toward where the story has them (to the hum, before the voice: slowly)
    if (!dusk(g) && !room.night) {
      const want = is(g, "edo.sonHeard") ? kOf(g) : K_HUM;
      const step = (dt / 1000) * (is(g, "edo.sonHeard") ? 0.02 : K_HUM / RISE_S);
      if (room.k < want) room.k = Math.min(want, room.k + step);
      if (Math.abs(room.drawn - room.k) > 0.002) { light(g); doors(g); }
    }
    if (!is(g, "edo.sonHeard") && !room.voice && room.k >= K_HUM && is(g, "edo.tomeHome") && idle(g)) g.run(() => voiceComes(g), { settle: false });
    const want = dusk(g) ? null : is(g, "edo.sonHeard") ? 1.2 : room.k >= K_HUM ? 0.8 : null;
    if (want !== room.hum) { if (want == null) { g.stopLoop("hum"); room.hum = null; } else if (g.loop("hum", { level: want })) room.hum = want; }
    // a game loaded with the talk done and the night not played: the night
    if (is(g, "edo.holdHands") && !is(g, "edo.nightDone") && !room.night && idle(g)) { room.night = true; g.run(() => g.cutscene("edo-night"), { settle: false }); }
  },

  picture: art + "back.png",
  // CUT-OUTS (the painter's plan): the dusk over the whole stage once the sun has gone (and the lattice's and the desk's dusk
  // twins); the west wall with the lattice (everyone in the hall in front of it, Ryōkai outside behind it, his face in the
  // gaps); the women's desk in front.
  planes: [
    { id: "dusk", src: art + "dusk.png", plane: "back", when: dusk },
    { id: "lattice", base: [[157, 349], [20, 444]], states: { day: art + "lattice.png", dusk: art + "lattice-dusk.png" }, state: (g) => (dusk(g) ? "dusk" : "day") },
    { id: "front", plane: "front", src: art + "front.png", states: { day: art + "front.png", dusk: art + "front-dusk.png" }, state: (g) => (dusk(g) ? "dusk" : "day") },
    { id: "near", src: art + "near.png", plane: "front" },
  ],
  // LIGHT (layout.json bars): the bars on the east wall (they climb: straight up, 82.9 px as k goes 0 to 1), on the floor (east
  // into the wall's foot, gone by k 0.372), and the shafts in the air (fading after k 0.8); each clipped and screen-blended over
  // the painting, under the people, as the keep's beams are. A script moves them (light()).
  live(kit, g) {
    const url = (file) => (g && g.assets && g.assets.url ? g.assets.url(art + file) : new URL("../../../" + art + file, import.meta.url).href);
    const img = (id, file) => `<image id="${id}" href="${url(file)}" x="0" y="0" width="800" height="600" style="image-rendering:pixelated"/>`;
    return `<defs><clipPath id="hall-clip-wall"><polygon points="559,343 799,526 799,263 559,228"/></clipPath>`
      + `<clipPath id="hall-clip-floor"><polygon points="0,599 0,458 157,349 554,339 799,526 799,599"/></clipPath></defs>`
      + `<g clip-path="url(#hall-clip-floor)" style="mix-blend-mode:screen">${img("hall-bars-floor", "bars-floor.png")}</g>`
      + `<g clip-path="url(#hall-clip-wall)" style="mix-blend-mode:screen">${img("hall-bars-wall", "bars-wall.png")}</g>`
      + `<g style="mix-blend-mode:screen">${img("hall-bars-air", "bars-air.png")}</g>`;
  },
  // THINGS THAT MOVE BY NATURE (layout.json fx): the hum's shimmer and the small door (portals: opened by the light and the
  // story), and the dust turning in the light while the sun is up. (The lamp and the incense are cold tonight: "No flame in
  // here tonight." Their flame and smoke are not lit.)
  fx: [
    { id: "hum", type: "portal", at: HUM, r: 14, wide: 0.7, keep: [559, 679], base: 414.5, pale: "#fff4d8", strength: 0.9, bend: 0.8, light: true },
    { id: "door", type: "portal", at: HUM, r: 19, wide: 0.7, keep: [559, 679], base: 415, pale: "#fff4d8", strength: 0.8, light: true },
    { id: "dust", type: "shimmer", poly: [[26, 368], [133, 239], [588, 287], [616, 298], [657, 314], [662, 316], [674, 321], [674, 413]], count: 26, size: 2, flow: [3, -0.4], life: 3.2,
      color: "#ffd8b0", opacity: 0.32, when: (g) => !dusk(g) },
  ],

  // O-Ume kneeling by the way out; Grandmother Tome just inside, going home as they come in; Ryōkai outside at the lattice.
  actors: [
    { id: "ume", kind: "ume-kneel", at: M.ume, face: "NE", life: { fidget: [6, 12], still: true } },
    { id: "tome", kind: "tome", at: TOME, face: "N", when: (g) => !is(g, "edo.tomeHome"), life: { fidget: false } },
    { id: "ryokai", kind: "ryokai-standing", at: RYOKAI, face: "E", life: { fidget: false } },
  ],

  // Back to front: a later area lies over an earlier one (layout.json things; the people's boxes against their figures).
  hotspots: [
    thing("ceiling", "ceiling", poly([[0, 0], [0, 121], [157, 154], [554, 157], [799, 100], [799, 0]]), M.mid, "N"),
    thing("slips", "name slips", poly([[254, 334], [469, 329], [469, 168], [254, 167]]), M.cabinet, "N"),
    // (the east wall's things are looked at from `big`, a step back: nobody stands by the wall in front of the hum)
    thing("wall", "east wall", poly([[563, 340], [799, 512], [799, 266], [563, 230]]), M.big, "NE"),
    // the bars of light on the east wall (where they climb; the shafts in the air are light, not a thing to click)
    thing("bars", "bars of light", poly([[572, 248], [694, 302], [694, 430], [572, 382]]), M.mid, "NE"),
    thing("posts", "posts", poly([[679, 434], [694, 446], [694, 125], [679, 128]]), M.big, "NE"),
    thing("lattice", "west lattice", poly([[132, 319], [14, 377], [14, 252], [132, 235]]), M.lattice, "W"),
    // the mats (the cushions' patch before the altar: a click elsewhere on the floor walks)
    thing("mats", "mats", poly([[286, 366], [444, 364], [450, 390], [280, 392]]), M.mats, "N"),
    thing("cabinet", "cabinet", poly([[335, 244], [338, 241], [387, 240], [388, 244], [388, 315], [335, 316]]), M.cabinet, "N", { use: cabinetUse }),
    thing("lamp", "lamp", poly([[384, 289], [393, 289], [394, 291], [394, 314], [384, 314], [384, 312]]), M.cabinet, "N"),
    thing("incense", "incense burner", poly([[355, 303], [356, 301], [368, 301], [368, 313], [368, 315], [355, 316]]), M.cabinet, "N"),
    thing("flowers", "flowers", poly([[326, 288], [327, 286], [346, 285], [346, 312], [345, 315], [326, 316]]), M.cabinet, "N"),
    thing("desk", "writing desk", poly([[0, 540], [160, 536], [166, 562], [150, 600], [0, 600]]), [180, 468], "SW", { plane: "front" }),
    thing("doorway", "doorway", poly([[170, 572], [799, 572], [799, 599], [170, 599]]), M.door, "S"),
    // the hum, and the small door in it once it is open (its three states: a coin, a hand, shut)
    { id: "hum", name: "place that hums", poly: HUM_POLY, walkTo: M.big, face: "NE", when: (g) => !is(g, "edo.sonHeard"), look: each("edo.hall.hum"), use: each("edo.hall.hum.use"), useWith: humWith },
    { id: "door", name: "small door", verb: "Talk into", poly: HUM_POLY, walkTo: M.big, face: "NE", when: (g) => is(g, "edo.sonHeard"), look: doorLook, use: doorUse, useWith: doorWith },
    // the people
    { id: "ume", name: "O-Ume", verb: "Talk to", rect: BOX.ume, walkTo: [206, 470], face: "W", look: each("edo.hall.ume"), use: (g) => talkTo(g, "ume", UME) },
    { id: "ryokai", name: "Ryōkai", verb: "Talk to", rect: BOX.ryokai, walkTo: M.lattice, face: "W", look: each("edo.hall.ryokai"), use: (g) => talkTo(g, "ryokai", RYO) },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and as the stage is built.
  setup(g) {
    room.voice = false; room.night = false; room.hum = null; room.humAt = null; room.doorAt = null;
    room.k = kOf(g); room.gone = is(g, "edo.holdHands") ? 1 : 0; room.drawn = -1;
    dressAll(g, "indoors", true);
    const r = g.actor("ryokai"), t = g.actor("tome");
    if (r) r.hold(true, "peer");
    if (t && t.sit) t.sit(false, true);                      // (Grandmother Tome's figure is found on the bench: on her feet here)
    const mom = g.actor("mom");
    if (mom && is(g, "edo.sonHeard") && !dusk(g)) { mom.face("E"); mom.kneel("back"); }
    const lil = g.actor("lilsis");
    if (lil && shining(g)) { lil.face("N"); lil.hold(true, "shine"); pinkLight(g, true); }
    light(g); doors(g);
  },

  async enter(g) {
    if (!is(g, "edo.tomeHome")) await enterHall(g);
  },
};

// (the names a test or a tool may want)
export const PLACES = { M, RYOKAI, TOME, TOME_OUT, HUM, BOX };
export { FLOOR, K_HUM, COIN, SON as sonTalk, UME as hallUmeTalk, RYO as hallRyokaiTalk, light as hallLight };

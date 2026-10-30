// Act Six, the third leg: inside the keep at Himeji, a lower floor (SCENES-20C: new in round twenty, in place of ENGINE-20's
// sketch; briefs/SCENES-20.md, and the design, briefs/out/edo-design.md, "edo-keep" and #29). Dim; the great pillar rising
// through the floor and the ceiling; the steep stairs; weapon racks along the right wall (spears and guns on pegs: scenery,
// never used); gun ports in the back wall, round, triangular and square, each throwing a beam of afternoon sun of its own
// shape across the floor; a stone-drop window; the plasterers' tubs. The young warden's post at the foot of the stairs up.
//
// The three of them come in with Tomezō's crew, counted at the gate (edo-castle.js, #28: edo.inside), at the mark `enter`,
// in the plasterers' white head-cloths.
//
//   #29 A Light That Needs No Fire   Shinnosuke at the foot of the stairs (shinnosukeTree, js/content/talk/edo-b.js): his
//                                    poems, five, seven and five (Big Sister counts on her fingers), the lady of the keep,
//                                    the dare, no fire in the keep. Little Sister shows him her pink flashlight (a light with
//                                    no fire: pink, on his face), and lends it (edo.lightShown, then edo.up): the lime may come
//                                    up, to carry the light. Then up the stairs, floor by floor, darker and steeper (CLIMB),
//                                    to the top floor (edo-keeptop.js), at sunset.
//   wrong tries                      the stairs while he is at them ("No one goes up. Except me. Tonight. Alone. With the
//                                    lady."), the gun ports, the weapon racks ("No."), the great pillar (Little Sister hugs it).
//
// The tree is WRITE-20B's, with one change of staging made here (ready.md lists it): the flashlight comes on in his face
// before his "...!", not after his four lines about it.
//
// Every place is the painter's own measurement of the finished picture (art/scenes/edo-keep/layout.json, PAINT-20E's
// ready.md), or was set by eye against the picture with the people in it; where the two differ the comment says why.
//
// Try it: index.html?scene=edo-keep&lead=lilsis&flags=edo.walked,edo.tomezoDown,edo.trowelBack,edo.crew,edo.inside

import { STOCK_DRESSED } from "./edo-common.js";
import { THREE, who, is, heard, each, idle, chatter, dressAll, TALK } from "./edo-himeji.js";
import { shinnosukeTree, CLIMB } from "../talk/edo-b.js";
import { scaleAt } from "../../engine/walk.js";

const art = "art/scenes/edo-keep/";

// ---------- the camera and the ground (layout.json: room.View, horizon 180, full 440; the lens 284 cm up) ----------
const HORIZON = 180, FULL = 440, MAX_SCALE = 1.2;      // (the floor's front edge, row 490, is 1.19 by the camera: nobody held smaller)
// The floor, from the back wall to row 490, less the stairs' footprint (the notch: the floor beyond the flight's open side,
// toward the left wall, is walkable, behind it).
const FLOOR = [[155, 354], [198, 354], [46, 485], [186, 485], [278, 354], [578, 354], [711, 485], [496, 485], [498, 490], [0, 490]];
const sizeAt = (y) => Math.min(MAX_SCALE, Math.max(0.26, (y - HORIZON) / (FULL - HORIZON)));

// ---------- the marks (layout.json marks) ----------
const M = { enter: [684, 479], pillar: [243, 427], racks: [611, 411], ports: [530, 464], tubs: [476, 487], stairs: [113, 488], drop: [579, 376], mid: [373, 435] };
const WARDEN = [243, 483];             // Shinnosuke's post at the foot of the stairs (marks.shinnosuke), facing W
const TO_WARDEN = [304, 480];          // where whoever talks to him stands: a pace to his right, turned to him
// The crew at work at the right, their backs to the stairs (the looks say so): Tomezō watching his men; one mixing in the
// back tub (behind it: the tubs are in front of everybody, base 599); one trowelling the right wall at its foot, under the
// racks (the wall's foot runs from (591, 362) to (760, 521)). The painter's mark for them is the doorway's (`enter`), where
// the three come in: they are set back from it, so that nobody comes in on top of them.
const CREW = { tomezo: [566, 440], plasterer1: [598, 463], plasterer2: [620, 404] };
// Where the three stand after the first few paces in (the open floor right of the beams' patches, facing the stairs).
const IN = { mom: [522, 476], bigsis: [474, 462], lilsis: [552, 488] };
// The flight (stairs.png): its foot (the mark), the bottom tread, and the top tread under the ceiling's opening; the floor
// under the flight goes back from row 469 to row 368 (its footprint, layout.json blocked), so a climber shrinks as he goes up
// and back. He is drawn on the flight: in front of the stairs (whose base line is [[186, 464], [257, 370]]).
const FLIGHT = { foot: [113, 488], bottom: [132, 452], top: [205, 128], from: 469, to: 368, base: 466 };
// The three beams of sun through the gun ports: light pictures (RGBA, keyed as frames), laid on the live layer with a screen
// blend; each beam's shaft of dusty air (layout.json beams[].air), for the dust in it.
const BEAMS = [
  { id: "beam-round", src: "beam-round.png", air: [[293, 429], [294, 426], [393, 224], [395, 220], [398, 217], [402, 215], [406, 214], [410, 215], [414, 217], [417, 220], [419, 224], [419, 228], [419, 232], [338, 419], [335, 423], [330, 426], [324, 429], [316, 432], [309, 433], [302, 434], [297, 433], [294, 432]] },
  { id: "beam-tri", src: "beam-tri.png", air: [[404, 413], [461, 240], [478, 210], [495, 240], [450, 413], [406, 438]] },
  { id: "beam-square", src: "beam-square.png", air: [[496, 435], [536, 214], [564, 214], [564, 241], [544, 412], [537, 435]] },
];
// The beams' slow travel as the sun sinks: about 0.4 px left and 1.6 px down a minute (layout.json fx.travel), from when the
// three came in; held to 12 px.
const TRAVEL = { dx: -0.4, dy: 1.6, most: 12 };

// ---------- what the floor is doing now that is not saved ----------
const room = { t0: 0, moved: [0, 0] };
const warden = (g) => g.actor("shinnosuke");
const atPost = (g) => !is(g, "edo.up") && !!warden(g);

// ---------- #29: Shinnosuke ----------
/** The hook `show` (staged here: the four lines about it said after the light is on): Little Sister holds out the pink
    flashlight and presses the end, and its light is on his face, pink; then his "...!". */
const LIGHT_LINES = [];
async function showLight(g) {
  const lil = g.actor("lilsis"), sh = warden(g);
  if (lil && sh) { lil.look(sh.x, sh.y); sh.look(lil.x, lil.y); }
  if (lil) lil.hold(true);                                                     // (it held out in front of her)
  g.sfx("click");
  let light = null;
  if (lil && sh) {
    const face = [sh.x - 2, sh.y - sh.h * sh.scale * 0.86], hand = [lil.x - 14 * lil.scale, lil.y - lil.h * lil.scale * 0.52];
    light = g.effects.add({ id: "pinklight", type: "mirror", target: face, mirror: hand, sizes: [[40, 7], [160, 12]], flat: 1.25, dim: 0, tremble: 0.6,
      image: null, color: "#ff9fd0", opacity: 0.5, on: 1, reach: [Math.min(hand[0], face[0]) - 10, Math.min(hand[1], face[1]) - 14, Math.abs(hand[0] - face[0]) + 20, Math.abs(hand[1] - face[1]) + 28], base: sh.y + 1 });
  }
  try { await g.say(...LIGHT_LINES); }
  finally {
    if (light) light.show(false);
    if (lil && lil.act && !lil.act.low) lil.hold(false);
  }
}
/** The hook `lend`: the light into his hands: he holds it in both hands from here to the end of the act. It is hers, lent. */
async function lend(g) {
  const lil = g.actor("lilsis"), sh = warden(g);
  if (lil && sh) lil.look(sh.x, sh.y);
  await g.reach();
  if (g.has("lilflash")) g.take("lilflash");
  g.sfx("pickup");
  if (sh) sh.hold(true, "light");
  if (!g.clock.skipping) g.ui.toast("Shinnosuke has the pink flashlight");
  await g.wait(300);
}
const WARDEN_TALK = (() => {
  const t = shinnosukeTree({ show: showLight, lend });
  const o = t.nodes.talk.options.find((x) => x.id === "light");
  LIGHT_LINES.push(...o.say); delete o.say;
  return t;
})();
async function wardenUse(g) {
  const sh = warden(g), lead = g.lead;
  if (sh && lead) { sh.look(lead.x, lead.y); lead.look(sh.x, sh.y); }
  const before = is(g, "edo.up");
  await g.talk(WARDEN_TALK);
  if (sh && sh.act && sh.act.low !== "light" && sh.act.low !== "kneel") sh.hold(false);
  if (!before && is(g, "edo.up")) await climb(g);
}

// ---------- the stairs, and the climb ----------
/** Someone up the flight: from the foot to the bottom tread, then up and back to the top tread (smaller as he goes back),
    and out of sight through the ceiling's opening. */
async function upFlight(g, id, delay) {
  const a = g.actor(id);
  if (!a) return;
  if (delay) await g.wait(delay);
  await a.walkPath(g.clock, [FLIGHT.foot, FLIGHT.bottom], sizeAt);
  a.base = FLIGHT.base;
  a.face("N");
  const [x0, y0] = FLIGHT.bottom, [x1, y1] = FLIGHT.top, s0 = sizeAt(FLIGHT.from), s1 = sizeAt(FLIGHT.to);
  if (!g.clock.skipping) {
    a.walking = true;
    try {
      await g.tween(2600, (k) => { a.place(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, s0 + (s1 - s0) * k); a.phase = (k * 7) % 1; if (k > 0.8) a.fade(1 - (k - 0.8) / 0.2); });
    } finally { a.walking = false; }
  }
  a.fade(0); a.hidden = true;
}
/** Up the stairs, floor by floor (the design: a short walk-through, not a puzzle): the warden first with the light, then
    Little Sister, Big Sister and Mom, short steps, up the flight and out of sight; then the dark of the floors above, the
    pink light going up through it and a line a floor (CLIMB: "Two." ... "Five."); and the top floor, at sunset, where Mom
    says "Six." (edo-keeptop.js, as they come up). */
async function climb(g) {
  const order = ["shinnosuke", "lilsis", "bigsis", "mom"].filter((id) => g.actor(id));
  for (const id of order) { const a = g.actor(id); if (a && a.act && id !== "shinnosuke") a.hold(false); }
  await Promise.all(order.map((id, n) => upFlight(g, id, n * 1100)));
  await g.fade(1, 700);
  // the floors above: nothing to see but the light with no fire, going up a floor a line
  g.ui.hud(false);
  g.view.clear();
  g.effects.drop();                                  // (the dust and the moth go with the floor; the top floor brings its own)
  const glow = `<defs><radialGradient id="climb-g"><stop offset="0" stop-color="#ffd2ea" stop-opacity="0.95"/><stop offset="0.35" stop-color="#ff9fd0" stop-opacity="0.5"/><stop offset="1" stop-color="#ff9fd0" stop-opacity="0"/></radialGradient></defs>
    <rect width="800" height="600" fill="#000"/><g id="climb-light" transform="translate(400 470)"><circle r="46" fill="url(#climb-g)"/><circle r="2.2" fill="#fff4fa"/></g>`;
  await g.view.draw("", "The stairs up through the keep, in the dark: only a small pink light going up.", { picture: null, live: glow, grid: [800, 600] });
  const light = g.q("#climb-light");
  await g.fade(0, 500);
  for (let n = 0; n < CLIMB.length - 1; n++) {
    const y0 = 470 - n * 70, y1 = y0 - 70;
    g.sfx("sandals");
    await g.tween(700, (k) => { if (light) light.setAttribute("transform", `translate(${400 + 18 * Math.sin((n + k) * 1.7)} ${y0 + (y1 - y0) * k})`); });
    await g.say(CLIMB[n]);
  }
  await g.fade(1, 600);
  g.flag("edo.climbed", true);
  // #30 is Mom's (the design: "Lead: Mom"): she comes up last, and the top floor is hers to begin with
  const d = g.store.data;
  if (d.active !== "mom" && d.team.includes("mom")) d.active = "mom";
  await g.goto("edo-keeptop", { spawn: "stairs", via: "fade", card: false });
}
/** The stairs: before he has the light, he is at their foot and nobody goes up; with it, up. */
async function stairsUse(g) {
  if (!is(g, "edo.up")) {
    if (atPost(g)) await g.say("edo.keep.stairs.no");
    return g.say(`edo.keep.stairs.use.${who(g)}`);
  }
  await g.say(`edo.keep.stairs.up.${who(g)}`);
  return climb(g);
}

// ---------- the crew at work, and what is said now and then ----------
const work = { next: {} };
const WORKERS = [["plasterer1", "mix", "mixing", 3900], ["plasterer2", "trowelwall", "trowelling", 4300]];
function workTick(g, dt) {
  if (!g.life || !g.life.enabled || g.dialogue.active || g.busy) return;
  for (const [id, hold, move, every] of WORKERS) {
    const a = g.actor(id);
    if (!a || a.hidden || a.walking) continue;
    work.next[id] = (work.next[id] ?? every) - dt;
    if (work.next[id] > 0) continue;
    work.next[id] = every + ((id.charCodeAt(9) * 53) % 1500);
    if (a.act && a.act.low === hold) a.hold(false);
    a.fidget(move).then(() => { if (g.actor(id) === a && !a.act && !a.walking) a.hold(true, hold); });
  }
}
/** The beams creep as the sun sinks (a few pixels in the minutes anyone spends here). */
function beamTick(g) {
  const mins = Math.max(0, ((g.store.data.playMs || 0) - room.t0) / 60000);
  const dx = Math.max(-TRAVEL.most, TRAVEL.dx * mins), dy = Math.min(TRAVEL.most, TRAVEL.dy * mins);
  if (Math.abs(dx - room.moved[0]) < 0.5 && Math.abs(dy - room.moved[1]) < 0.5) return;
  room.moved = [dx, dy];
  for (const b of BEAMS) { const el = g.q(`#${b.id}`); if (el) el.setAttribute("transform", `translate(${dx.toFixed(1)} ${dy.toFixed(1)})`); }
}
const CHAT = chatter([
  { when: (g) => !is(g, "edo.up") && !heard(g, "edo.keep.plasterer.2"), say: ["edo.keep.plasterer.2"] },      // (once)
], { first: [26, 34], every: [60, 90], when: (g) => !!g.actor("plasterer2") });

// ---------- the scene ----------
/** A thing of the floor, by its shape, with a look and a use for each of the three. */
const thing = (id, name, shape, walkTo, face, more = {}) => ({ id, name, ...shape, walkTo, face, look: each(`edo.keep.${id}`), use: each(`edo.keep.${id}.use`), ...more });

export default {
  id: "edo-keep",
  era: "edo",
  name: "Inside the keep",
  music: "edo-keep",

  horizon: HORIZON, full: FULL, maxScale: MAX_SCALE,
  walk: { area: FLOOR },
  // the pillar's foot, the stairs' footprint, the tubs and the lime (layout.json blocked)
  blocked: [[[239, 381], [307, 381], [295, 407], [218, 407]], [[182, 368], [264, 368], [191, 469], [64, 469]], [[499, 493], [763, 493], [799, 599], [535, 599]]],

  party: THREE,
  spawn: { default: M.enter, ...M },
  arrive: { enter: [[652, 466], [636, 482]] },
  facing: "W",
  stock: STOCK_DRESSED,
  talk: TALK,
  tick(g, dt) { workTick(g, dt); beamTick(g); CHAT.tick(g, dt); },

  picture: art + "back.png",
  // CUT-OUTS, back to front (the painter's plan): the racks on the right wall (nobody passes behind them), the stairs (their
  // open side: the floor beyond is behind them), the great pillar, the tubs (in front of everybody), the plasterers' plank,
  // buckets and brushes at the bottom left (front).
  planes: [
    { id: "racks", src: art + "racks.png", base: [[760, 521], [591, 362]] },
    { id: "stairs", src: art + "stairs.png", base: [[186, 464], [257, 370]] },
    { id: "pillar", src: art + "pillar.png", base: 407 },
    { id: "tubs", src: art + "tubs.png", base: 599 },
    { id: "front", src: art + "front.png", plane: "front" },
  ],
  // LIGHT: the three beams of sun through the gun ports, round, triangular and square (their shafts and their patches on the
  // floor), laid over the painting with a screen blend; under the people, as the live layer is.
  live(kit, g) {
    const url = (file) => (g && g.assets && g.assets.url ? g.assets.url(art + file) : new URL("../../../" + art + file, import.meta.url).href);
    return BEAMS.map((b) => `<image id="${b.id}" href="${url(b.src)}" width="800" height="600" style="mix-blend-mode:screen;image-rendering:pixelated"/>`).join("");
  },
  // THINGS THAT MOVE BY NATURE: dust turning in each beam; and a moth now and then across the beams.
  fx: [
    ...BEAMS.map((b, n) => ({ id: `dust-${n + 1}`, type: "shimmer", poly: b.air, count: 9, size: 2, flow: [-1.2, 3.2], life: 3.2, color: "#fff4d6", opacity: 0.42, seed: 11 + n })),
    { id: "moth", type: "birds", lanes: [[[300, 240], [520, 300]], [[560, 260], [380, 330]]], every: [20, 50], group: [1, 1], size: 3, speed: 30, color: "#c8b890", seed: 4 },
  ],

  // The warden at his post (until he goes up with the light), and three of the crew at their work by the tubs.
  actors: [
    { id: "shinnosuke", kind: "shinnosuke", at: WARDEN, face: "W", when: (g) => !is(g, "edo.up"), life: { fidget: [3, 7], still: true } },
    { id: "tomezo", kind: "tomezo", at: CREW.tomezo, face: "E", life: { fidget: [6, 12], still: true } },
    { id: "plasterer1", kind: "plasterer1", at: CREW.plasterer1, face: "SE", life: { fidget: false } },
    { id: "plasterer2", kind: "plasterer2", at: CREW.plasterer2, face: "E", life: { fidget: false } },
  ],

  // Back to front: a later area lies over an earlier one (layout.json things; the cut-outs' own outlines where the painter
  // gave a silhouette: tools' measure of their pictures).
  hotspots: [
    thing("ceiling", "ceiling", { poly: [[142, 123], [598, 123], [800, 0], [0, 0]] }, M.mid, "N"),
    thing("beams", "beams of sun", { poly: [[293, 429], [294, 426], [393, 224], [395, 220], [398, 217], [402, 215], [406, 214], [478, 210], [564, 214], [564, 241], [544, 412], [537, 435], [406, 438], [302, 434], [297, 433], [294, 432]] }, M.ports, "N"),
    thing("ports", "gun ports", { poly: [[386, 206], [572, 206], [572, 248], [386, 248]] }, M.ports, "N"),
    thing("portround", "round gun port", { poly: [[419, 228], [419, 224], [417, 220], [414, 217], [410, 215], [406, 214], [402, 215], [398, 217], [395, 220], [393, 224], [393, 228], [393, 232], [395, 235], [398, 238], [402, 240], [406, 241], [410, 240], [414, 238], [417, 235], [419, 232]] }, M.ports, "N"),
    thing("porttri", "triangular gun port", { poly: [[478, 206], [499, 242], [457, 242]] }, M.ports, "N"),
    thing("portsquare", "square gun port", { poly: [[536, 241], [564, 241], [564, 214], [536, 214]] }, M.ports, "N"),
    thing("drop", "stone-drop window", { poly: [[552, 344], [596, 344], [610, 366], [560, 366]] }, M.drop, "N"),
    thing("racks", "weapon racks", { poly: [[591, 274], [592, 194], [621, 187], [632, 185], [716, 185], [740, 204], [773, 260], [773, 268], [770, 405], [768, 496], [767, 519], [757, 519], [648, 416], [591, 361]] }, M.racks, "E", { plane: "racks" }),
    thing("pillar", "great pillar", { poly: [[227, 106], [229, 104], [241, 102], [274, 102], [293, 104], [302, 107], [302, 393], [298, 399], [282, 406], [271, 408], [243, 408], [235, 406], [228, 401], [227, 398]] }, M.pillar, "N", { plane: "pillar" }),
    thing("stairs", "stairs up", { poly: [[80, 437], [128, 283], [181, 115], [254, 61], [255, 61], [256, 65], [257, 73], [258, 121], [258, 129], [254, 370], [188, 462], [180, 465], [80, 465]] }, M.stairs, "N",
      { plane: "stairs", verb: "Go up", use: stairsUse }),
    thing("tubs", "plasterers' tubs", { poly: [[530, 528], [532, 521], [564, 466], [582, 458], [705, 450], [756, 451], [798, 485], [800, 509], [799, 552], [602, 599], [580, 599], [550, 588], [535, 575], [531, 565]] }, M.tubs, "E", { plane: "tubs" }),
    // the floor, where it is not walked on: in front of the walk, between the plank at the left and the tubs
    thing("floor", "floor", { poly: [[262, 494], [528, 494], [534, 600], [244, 600], [262, 524]] }, M.mid, "S"),
    // the crew, at work at the right (the one area for the three of them)
    { id: "crew", name: "plasterers", poly: [[586, 352], [726, 352], [726, 482], [586, 482]], walkTo: [600, 470], face: "E", look: each("edo.keep.crew"), use: each("edo.keep.crew.use") },
    // the warden, at the foot of the stairs
    { id: "shinnosuke", name: "Shinnosuke", verb: "Talk to", rect: [218, 318, 50, 166], walkTo: TO_WARDEN, face: "W", look: each("edo.keep.shinnosuke"), use: wardenUse,
      useWith: { lilflash: wardenUse }, when: (g) => !is(g, "edo.up") },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and as the stage is built.
  setup(g) {
    dressAll(g, "edo-crew");
    { const a = g.actor("plasterer1"); if (a) a.hold(true, "mix"); }
    { const a = g.actor("plasterer2"); if (a) a.hold(true, "trowelwall"); }
    work.next = {};
    room.t0 = g.store.data.playMs || 0; room.moved = [0, 0];
    CHAT.reset();
  },

  // Coming in with the crew, the first time: the buckets go to the tubs, and the three walk a few paces in, out of the
  // crew's way (they come in by the doorway at the right edge, among the tubs: layout.json's notes), and look at the room.
  async enter(g) {
    if (heard(g, "edo.keep.plasterer.1") || !g.actor("plasterer1")) return;
    await g.wait(300);
    await g.say("edo.keep.plasterer.1");
    await Promise.all(THREE.map((id, n) => (g.actor(id) ? g.wait(n * 260).then(() => g.walkTo(...IN[id], id)).then(() => { const a = g.actor(id); if (a) a.face("W"); g.rememberPlace(id); }) : null)));
  },
};

export const PLACES = { M, WARDEN, TO_WARDEN, CREW, FLIGHT };
export { WARDEN_TALK as wardenTalk, climb };

// Act One, the third of four scenes: inside the pyramid, the great rising gallery.
// Egypt, about 1920 B.C. (the Bible's own count of years: briefs/DATING.md). Dad plays.
//
// Awe first, then comedy. The passage from outside comes in at the foot on the left; the ramp climbs to a
// small doorway at the top (to egypt-chamber). The lamp boy sits at the foot and will not go up again.
//
//   chain B   The lamp boy is the only one who SAW it: a small one with a little sun in his hand pointed it at
//             the wall, and the wall opened like an eye and took him. That is the clue that light does it.
//   chain C2  The door mirror off the wagon, wedged in the slot at the foot, turns the sunbeam up the ramp.
//   chain C3  The goldsmith's copper mirror, stood on the step at the top, turns it in at the doorway.
//
// The sunbeam is drawn live, a stretch at a time, and a stretch shows only when everything before it is in
// place: in at the passage (the shade is up outside), up the ramp (and the door mirror is in), in at the top
// (and the copper mirror is up). A mirror put in out of order does nothing yet, and Dad says why.
//
// Try it: index.html?scene=egypt-gallery&lead=dad
// Later states: &flags=egypt.arrived,egypt.inside,egypt.sawGallery,egypt.knowsLight,egypt.shadeSet,egypt.footSet

const art = "art/scenes/egypt-gallery/";

/** How many times a line has been spoken. (The engine counts every line it says.) */
const count = (g, id) => g.store.data.seenLines[id] || 0;
/** A thing worth looking at twice: the first line, then the second, turn about. */
const twice = (first, second) => (g) => g.say(count(g, first) <= count(g, second) ? first : second);

/** How far the sunbeam gets: 0 not in at all, 1 as far as the foot of the ramp, 2 up to the top step, 3 into the chamber. */
const sunReach = (g) => (!g.flag("egypt.shadeSet") ? 0 : !g.flag("egypt.footSet") ? 1 : !g.flag("egypt.topSet") ? 2 : 3);

// ---------- light: the sunbeam in three stretches ----------
// The painter's marks for the beam: in through the lit opening (by 193, 450), to the mirror in the slot (531, 409),
// up to the mirror on the top step (400, 176), and in at the doorway right behind it.
const BEAM_IN = [[166, 439], [170, 467], [532, 416], [530, 402]];     // the soft outer light: from the edge of the opening in the left wall across to the slot
const CORE_IN = [[167, 448], [169, 458], [531, 411.5], [531, 406.5]]; // its bright middle
const BEAM_UP = [[525, 412], [537, 406], [403, 174], [397, 178]];     // from the slot up the ramp to the top step (it narrows as it climbs, as the people do)
const CORE_UP = [[529, 410], [533, 408], [401, 175.5], [399, 176.5]];
const SPILL = [541, 426, 24, 15];                                     // where the beam lands on bare stone, before there is a mirror in the slot (cx, cy, rx, ry)
const TOP = [400, 172, 20, 24];                                       // the doorway at the top, lit: the last stretch is too short to see as a beam
// (The lamps' flames were drawn here as soft ellipses until round four; they are the engine's `flame` now: see `fx`.)
const points = (shape) => shape.map((p) => p.join(",")).join(" ");
const beam = (id, outer, core) => `<g id="${id}" opacity="0" shape-rendering="geometricPrecision">
  <polygon points="${points(outer)}" fill="#ffe7a0" opacity="0.3" filter="url(#sun-soft)"/><polygon points="${points(core)}" fill="#fff4c8" opacity="0.55" filter="url(#sun-edge)"/></g>`;
/** Show or hide a part of the light at once (setup), or bring it up over a moment (scripts). */
const lit = (g, id, on) => { const el = g.q("#" + id); if (el) el.setAttribute("opacity", on ? 1 : 0); };
const glow = (g, id, ms = 900) => { const el = g.q("#" + id); return el ? g.tween(ms, (k) => el.setAttribute("opacity", k)) : Promise.resolve(); };

/** Make the light match the story facts. */
function dress(g) {
  const far = sunReach(g);
  lit(g, "beam-in", far >= 1);
  lit(g, "beam-spill", far === 1);
  lit(g, "beam-up", far >= 2);
  lit(g, "beam-out", far >= 3);
}

// ---------- chain B: the lamp boy ----------
async function whatHeSaw(g) {
  await g.say("egypt.ask.boy", "egypt.lampboy.saw.1", "egypt.lampboy.saw.ask", "egypt.lampboy.saw.2", "egypt.lampboy.saw.3", "egypt.lampboy.saw.4");
  // What Dad makes of it depends on what he has found out, and on what he has in his pockets.
  await g.say(g.flag("egypt.knowsLight") ? "egypt.lampboy.saw.5c" : g.has("flashlight") ? "egypt.lampboy.saw.5b" : "egypt.lampboy.saw.5a");
  g.flag("egypt.heardBoy", true);
}

async function talkToBoy(g) {
  if (!g.flag("egypt.metBoy")) {
    await g.say("egypt.lampboy.meet.1", "egypt.lampboy.meet.2");
    g.flag("egypt.metBoy", true);
  }
  for (;;) {
    const pick = await g.choose([
      { id: "boy", line: "egypt.ask.boy" },
      { id: "door", line: "egypt.ask.door", when: (g) => !!g.flag("egypt.heardBoy") },
      { id: "lamps", line: "egypt.lampboy.ask.lamps" },
      { id: "bye", line: "egypt.lampboy.ask.bye" },
    ]);
    if (pick === "boy") await whatHeSaw(g);
    else if (pick === "door") await g.say("egypt.ask.door", "egypt.lampboy.door.1", "egypt.lampboy.door.2", "egypt.lampboy.door.3");
    else if (pick === "lamps") await g.say("egypt.lampboy.ask.lamps", "egypt.lampboy.lamps.1", "egypt.lampboy.lamps.2", "egypt.lampboy.lamps.3");
    else return g.say("egypt.lampboy.ask.bye", "egypt.lampboy.bye");
  }
}

/** General Feathers, shown to the boy who feeds the lamps: he wants to know what she eats. He asks once; after that,
    Dad's stock reply. */
async function showGeneral(g) {
  if (count(g, "egypt.lampboy.chicken")) return g.say("egypt.chicken.stock");
  await g.say("egypt.chicken.show", "egypt.lampboy.chicken", "egypt.lampboy.chicken.2");
}

/** The flashlight, shown to the boy. Alight, he wants nothing to do with it. Dead, it is a lamp, and lamps are his trade. */
async function showFlashlight(g) {
  if (!g.flag("egypt.knowsLight")) return g.say("egypt.lampboy.flashlight");
  await g.say("egypt.lampboy.dead.1");
  await g.reach();
  g.take("flashlight");
  await g.say("egypt.lampboy.dead.2", "egypt.lampboy.dead.3");
}

// ---------- chain C2: the door mirror, in the slot at the foot ----------
async function wedgeMirror(g) {
  await g.reach();
  g.take("carmirror");
  g.flag("egypt.footSet", true);                  // the mirror appears in the slot (its cut-out follows the fact)
  lit(g, "beam-spill", false);
  await g.say("egypt.foot.set");
  if (!g.flag("egypt.shadeSet")) return g.say("egypt.mirror.nothing");
  await glow(g, "beam-up");
  if (g.flag("egypt.topSet")) { await glow(g, "beam-out", 500); await g.say("egypt.relay.done"); }
  else await g.say("egypt.foot.lit");
  g.flag("egypt.beamSeen", sunReach(g));
}

// ---------- chain C3: the copper mirror, on the step at the top ----------
async function standMirror(g) {
  if (!g.flag("egypt.knowsLight")) return g.say("egypt.top.early");      // (he can have the mirror before he knows what a mirror is for)
  await g.reach();
  g.take("coppermirror");
  g.flag("egypt.topSet", true);                   // the mirror appears on the step
  await g.say("egypt.top.set");
  if (sunReach(g) < 3) return g.say("egypt.top.dark");
  await glow(g, "beam-out", 500);
  await g.say("egypt.top.lit");
  g.flag("egypt.beamSeen", 3);
}

export default {
  id: "egypt-gallery",
  era: "egypt",
  name: "The great gallery",

  // Every number below is a pixel of the painting, measured by the painter (art/scenes/egypt-gallery/layout.json).
  // DEPTH: people shrink a lot as they climb, to a third of their size at the top.
  horizon: 50, full: 580,

  // The level floor at the foot, and the ramp up the middle to the tall step. The cut in the foot of the ramp,
  // which leads down to the low passage, is a pit: nobody walks into it.
  walk: { area: [[179, 595], [227, 522], [314, 522], [318, 499], [366, 225], [433, 226], [484, 500], [491, 521], [527, 521], [562, 594]] },
  blocked: [[[364, 500], [437, 501], [426, 374], [374, 375]]],
  spawn: {
    default: [263, 541],
    fromSite: [263, 541],           // in from the lit opening on the left
    fromChamber: [400, 232],        // down from the doorway at the top
  },
  exits: ["egypt-site", "egypt-chamber"],
  // The left of the picture is the way out to the daylight (the lit opening in the left wall), and the top of it is the
  // way up the ramp to the doorway at the top. The long stair outside is walked whole only once, so the way out comes
  // down it the first time and is found halfway down after that, as through the opening itself.
  edges: {
    W: { to: "egypt-site", name: "outside", walkTo: [239, 542], use: (g) => g.goto("egypt-site", { spawn: g.flag("egypt.cameDown") ? "fromGalleryAgain" : "fromGallery" }) },
    N: { to: "egypt-chamber", spawn: "fromGallery", name: "up the ramp", walkTo: [400, 231] },
  },

  picture: art + "back.png",

  planes: [
    { id: "mirror-top", src: art + "mirror-top.png", base: 194, when: (g) => !!g.flag("egypt.topSet") },
    { id: "mirror-foot", src: art + "mirror-foot.png", base: 471, when: (g) => !!g.flag("egypt.footSet") },
    { id: "front", src: art + "front.png", plane: "front" },
  ],

  // The light here: the sunbeam, where it spills on the bench, and the doorway at the top when the sun gets there. All of
  // the beam starts hidden; dress() shows what the facts say, and the scripts above bring a new stretch up. (The lamps'
  // flames are in `fx`, below.)
  live() {
    return `<defs><filter id="sun-soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
        <filter id="sun-edge" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.6"/></filter></defs>
      ${beam("beam-in", BEAM_IN, CORE_IN)}
      <ellipse id="beam-spill" opacity="0" cx="${SPILL[0]}" cy="${SPILL[1]}" rx="${SPILL[2]}" ry="${SPILL[3]}" fill="#fff3c4" filter="url(#sun-soft)" shape-rendering="geometricPrecision"/>
      ${beam("beam-up", BEAM_UP, CORE_UP)}
      <g id="beam-out" opacity="0" shape-rendering="geometricPrecision">
        <ellipse cx="${TOP[0]}" cy="${TOP[1]}" rx="${TOP[2] + 12}" ry="${TOP[3] + 12}" fill="#ffe7a0" opacity="0.45" filter="url(#sun-soft)"/>
        <ellipse cx="${TOP[0]}" cy="${TOP[1]}" rx="${TOP[2]}" ry="${TOP[3]}" fill="#fff8dc" opacity="0.8" filter="url(#sun-soft)"/>
      </g>`;
  },

  // THINGS THAT MOVE BY NATURE (round four: briefs/out/paint-4b-ready.md). The painted tongues of the eight lamps are gone
  // (the lamplight on the stone, the glow round each flame, the light in the oil and the soot stay painted), and the
  // engine draws each flame on its wick, flickering, at its lamp's depth: a man passing in front of a lamp covers it.
  // The lamp on the bench at the front right is on the front plane. (`at`: the wick; `size`: how tall the painted flame stood.)
  fx: [
    // [at x, at y, base, size, width, lean]: lamps 1 to 5 on the benches up the ramp, 6 on the floor, 7 by the boy, 8 at the front
    [282.6, 374.7, 377, 10.3, 6.2, -0.4], [326.1, 252.9, 254, 6.5, 3.9, -0.3], [337, 220.2, 221, 5.5, 3.3, -0.2], [496.2, 299.7, 302, 8, 4.8, -0.3],
    [466.9, 221.2, 222, 5.5, 3.3, -0.2], [309.2, 512.2, 515, 14.1, 8.4, -0.6], [560, 468.3, 472, 14.2, 8.5, -0.6], [641.2, 555.3, "front", 20, 12, -0.8],
  ].map(([x, y, base, size, width, lean], n) => ({ id: `lamp-${n + 1}`, type: "flame", at: [x, y], base, size, width, edge: "#f08a1c", color: "#ffd45a", glowOpacity: 0.12, lean })),

  actors: [
    // On the front edge of the stone bench, his legs hanging. He will not go up the ramp again; but now and then he gets
    // up (his jar of oil with him) to see to the lamp beside him, or steps out to the foot of the ramp and looks up it, and
    // comes back to his bench. His mark is on the bench, off the floor: he walks straight there and back.
    { id: "lampboy", kind: "lampboy", at: [582, 586], face: "SW",
      life: { every: [20, 38], spots: [[522, 532, "NE"], [500, 566, "N"]], stay: [3, 6] } },
  ],

  setup: dress,

  // The far things first: an area lower in this list lies over the ones above it. Each shape follows its thing's own
  // edge, within a few pixels; the ladder is a cut-out and the lamp boy a person, and Show outlines their own silhouettes.
  // The walls leave the top of the picture to the way up the ramp, and its left edge to the way out.
  hotspots: [
    { id: "wall-left", name: "gallery walls", poly: [[44, 60], [340, 60], [333, 192], [300, 240], [268, 300], [245, 350], [225, 388], [164, 431], [164, 593], [157, 600], [44, 600]], look: twice("egypt.gallery.walls.look", "egypt.gallery.walls.look2") },
    { id: "wall-right", name: "gallery walls", poly: [[460, 60], [800, 60], [800, 600], [700, 600], [640, 540], [600, 470], [570, 420], [555, 370], [530, 310], [505, 250], [475, 195]], look: twice("egypt.gallery.walls.look", "egypt.gallery.walls.look2") },
    {
      id: "top-door", name: "doorway at the top", verb: "Go through", poly: [[381, 152], [419, 152], [419, 197], [381, 197]], walkTo: [400, 231], face: "N",
      look: (g) => g.say(g.flag("egypt.sawChamber") ? "egypt.gallery.top.look2" : "egypt.gallery.top.look"),
      use: (g) => g.goto("egypt-chamber", { spawn: "fromGallery" }),
    },
    {
      id: "step-top", name: "top step", poly: [[364, 198], [436, 198], [438, 206], [361, 206]], walkTo: [395, 230], face: "N",
      look: (g) => g.say(g.flag("egypt.topSet") ? "egypt.gallery.step.set" : "egypt.gallery.step.look"),
      useWith: { coppermirror: standMirror, carmirror: "egypt.top.wrong", shade: "egypt.gallery.shade" },
    },
    { id: "chest", name: "chest", poly: [[455, 236], [475, 236], [484, 258], [483, 277], [455, 277], [452, 258]], walkTo: [431, 306], face: "E", look: "egypt.gallery.chest.look" },      // the chest, and the two jars of white stone above it
    { id: "dinner", name: "bread and beer", poly: [[290, 320], [300, 317], [310, 322], [315, 333], [324, 337], [326, 349], [318, 355], [300, 354], [290, 343]], walkTo: [355, 380], face: "W", look: "egypt.gallery.dinner.look" },
    { id: "sledge-runner", name: "sledge runner", poly: [[465, 299], [479, 297], [497, 410], [484, 413]], walkTo: [460, 413], face: "E", look: "egypt.gallery.runner.look" },
    { id: "marks", name: "builders' marks", poly: [[571, 338], [584, 337], [592, 358], [599, 362], [616, 363], [618, 394], [626, 417], [624, 432], [614, 428], [598, 414], [574, 392], [570, 360]], walkTo: [501, 538], face: "E", look: twice("egypt.gallery.marks.look", "egypt.gallery.marks.look2") },
    {
      id: "low-passage", name: "low passage", verb: "Look into", poly: [[376, 389], [425, 389], [425, 438], [376, 438]], walkTo: [400, 511], face: "N",
      look: "egypt.gallery.low.look", use: "egypt.gallery.low.use",
      useWith: { flashlight: (g) => g.say(g.flag("egypt.knowsLight") ? "egypt.flash.dead" : "egypt.gallery.low.flashlight") },
    },
    {
      id: "slot-foot", name: "slot in the bench", poly: [[518, 396], [553, 394], [557, 415], [562, 422], [560, 452], [528, 452], [522, 422]], walkTo: [462, 471], face: "E",      // the slot, and the mirror once it is in
      look: (g) => g.say(g.flag("egypt.footSet") ? "egypt.gallery.slot.set" : g.flag("egypt.shadeSet") ? "egypt.gallery.slot.beam" : "egypt.gallery.slot.look"),
      useWith: { carmirror: wedgeMirror, coppermirror: "egypt.foot.wrong", shade: "egypt.gallery.shade" },
    },
    { id: "oil-jars", name: "oil jars", verb: "Borrow", poly: [[233, 446], [243, 440], [256, 442], [262, 452], [268, 446], [278, 447], [283, 462], [284, 492], [300, 492], [302, 503], [314, 508], [313, 519], [296, 519], [285, 513], [262, 513], [247, 516], [234, 508], [230, 470]], walkTo: [316, 529], face: "W", look: "egypt.gallery.jars.look", use: "egypt.gallery.jars.use" },
    { id: "rope", name: "coil of rope", poly: [[533,511], [530,516], [522,520], [510,521], [498,520], [490,516], [487,511], [490,506], [498,502], [510,501], [522,502], [530,506]], walkTo: [475, 527], face: "E", look: "egypt.gallery.rope.look" },
    {
      id: "way-out", name: "way out", verb: "Take the", poly: [[164, 593], [222, 511], [221, 389], [164, 431]], walkTo: [239, 542], face: "W",
      look: "egypt.gallery.out.look", use: (g) => g.goto("egypt-site", { spawn: g.flag("egypt.cameDown") ? "fromGalleryAgain" : "fromGallery" }),      // (the long stair outside is walked whole only once)
    },
    { id: "ladder", name: "ladder", plane: "front", poly: [[97, 241], [108, 241], [131, 243], [138, 247], [157, 600], [92, 600]], walkTo: [210, 569], face: "W", look: "egypt.gallery.ladder.look" },
    {
      id: "lampboy", name: "lamp boy", verb: "Talk to", poly: [[582, 475], [572, 477], [568, 483], [571, 498], [566, 502], [556, 537], [549, 548], [549, 577], [542, 582], [546, 588], [554, 587], [559, 591], [569, 589], [572, 586], [573, 558], [592, 549], [596, 543], [595, 506], [587, 497], [590, 482]], walkTo: [510, 572], face: "E",
      look: "egypt.lampboy.look", use: talkToBoy,
      useWith: { flashlight: showFlashlight, rootbeer: "egypt.lampboy.rootbeer", sunglasses: "egypt.lampboy.sunglasses", chicken: showGeneral },
    },
  ],

  // Runs when the lead arrives. It must be safe to run twice, so each part checks its own fact.
  async enter(g) {
    if (!g.flag("egypt.sawGallery")) {
      await g.wait(400);
      await g.say("egypt.gallery.arrive.1", "egypt.gallery.arrive.2");
      g.flag("egypt.sawGallery", true);
    }
    // The first time he sees how far the sunbeam has got since he was last here, he says so. (A mirror he
    // placed here himself has had its say already: "egypt.beamSeen" is how far he has seen it get.)
    const far = sunReach(g);
    if (far > (g.flag("egypt.beamSeen") || 0)) {
      await g.say(["egypt.beam.in", "egypt.beam.up", "egypt.relay.done"][far - 1]);
      g.flag("egypt.beamSeen", far);
      if (!g.flag("egypt.boySawSun")) { await g.say("egypt.lampboy.sun"); g.flag("egypt.boySawSun", true); }
    }
  },
};

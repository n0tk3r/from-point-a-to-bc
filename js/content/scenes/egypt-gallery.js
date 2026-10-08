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

// ---------- light: the sunbeam in three stretches, and the lamps ----------
// The painter's marks for the beam: in through the lit opening (by 193, 450), to the mirror in the slot (531, 409),
// up to the mirror on the top step (400, 176), and in at the doorway right behind it.
const BEAM_IN = [[166, 439], [170, 467], [532, 416], [530, 402]];     // the soft outer light: from the edge of the opening in the left wall across to the slot
const CORE_IN = [[167, 448], [169, 458], [531, 411.5], [531, 406.5]]; // its bright middle
const BEAM_UP = [[525, 412], [537, 406], [403, 174], [397, 178]];     // from the slot up the ramp to the top step (it narrows as it climbs, as the people do)
const CORE_UP = [[529, 410], [533, 408], [401, 175.5], [399, 176.5]];
const SPILL = [541, 426, 24, 15];                                     // where the beam lands on bare stone, before there is a mirror in the slot (cx, cy, rx, ry)
const TOP = [400, 172, 20, 24];                                       // the doorway at the top, lit: the last stretch is too short to see as a beam
const LAMPS = [[283, 371, 0.61], [326, 251, 0.38], [337, 218, 0.32], [496, 297, 0.47], [467, 219, 0.32], [309, 507, 0.83], [560, 463, 0.84], [641, 546, 1.18]];   // each flame, and how big things are there
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

  picture: art + "back.png",

  planes: [
    { id: "mirror-top", src: art + "mirror-top.png", base: 194, when: (g) => !!g.flag("egypt.topSet") },
    { id: "mirror-foot", src: art + "mirror-foot.png", base: 471, when: (g) => !!g.flag("egypt.footSet") },
    { id: "front", src: art + "front.png", plane: "front" },
  ],

  // Everything here is light: the sunbeam, where it spills on the bench, the doorway at the top when the sun gets
  // there, and the lamp flames. All of the beam starts hidden; dress() shows what the facts say, and the scripts above
  // bring a new stretch up. The painting has the lit stone round each lamp; the game adds a flame that will not keep still.
  live() {
    const flame = ([x, y, k], n) => `<ellipse cx="${x}" cy="${y - 2 * k}" rx="${9 * k}" ry="${11 * k}" fill="#ffc266" opacity="0.5" filter="url(#lamp-soft)"/>` +
      `<ellipse class="flicker" cx="${x}" cy="${y - 3 * k}" rx="${5 * k}" ry="${7 * k}" fill="#ffe9b0" opacity="0.8" filter="url(#lamp-soft)" style="animation-delay:${-0.37 * n}s"/>`;
    return `<defs><filter id="sun-soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
        <filter id="sun-edge" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.6"/></filter>
        <filter id="lamp-soft" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="2.5"/></filter></defs>
      <g shape-rendering="geometricPrecision">${LAMPS.map(flame).join("")}</g>
      ${beam("beam-in", BEAM_IN, CORE_IN)}
      <ellipse id="beam-spill" opacity="0" cx="${SPILL[0]}" cy="${SPILL[1]}" rx="${SPILL[2]}" ry="${SPILL[3]}" fill="#fff3c4" filter="url(#sun-soft)" shape-rendering="geometricPrecision"/>
      ${beam("beam-up", BEAM_UP, CORE_UP)}
      <g id="beam-out" opacity="0" shape-rendering="geometricPrecision">
        <ellipse cx="${TOP[0]}" cy="${TOP[1]}" rx="${TOP[2] + 12}" ry="${TOP[3] + 12}" fill="#ffe7a0" opacity="0.45" filter="url(#sun-soft)"/>
        <ellipse cx="${TOP[0]}" cy="${TOP[1]}" rx="${TOP[2]}" ry="${TOP[3]}" fill="#fff8dc" opacity="0.8" filter="url(#sun-soft)"/>
      </g>`;
  },

  actors: [
    { id: "lampboy", kind: "lampboy", at: [582, 586], face: "SW" },       // on the front edge of the stone bench, his legs hanging
  ],

  setup: dress,

  // The far things first: an area lower in this list lies over the ones above it.
  hotspots: [
    { id: "walls", name: "gallery walls", rect: [100, 0, 600, 150], look: twice("egypt.gallery.walls.look", "egypt.gallery.walls.look2") },
    {
      id: "top-door", name: "doorway at the top", verb: "Go through", rect: [377, 150, 46, 48], walkTo: [400, 231], face: "N",
      look: (g) => g.say(g.flag("egypt.sawChamber") ? "egypt.gallery.top.look2" : "egypt.gallery.top.look"),
      use: (g) => g.goto("egypt-chamber", { spawn: "fromGallery" }),
    },
    {
      id: "step-top", name: "top step", rect: [361, 192, 77, 13], walkTo: [395, 230], face: "N",
      look: (g) => g.say(g.flag("egypt.topSet") ? "egypt.gallery.step.set" : "egypt.gallery.step.look"),
      useWith: { coppermirror: standMirror, carmirror: "egypt.top.wrong", shade: "egypt.gallery.shade" },
    },
    { id: "chest", name: "chest", rect: [456, 227, 21, 64], walkTo: [431, 306], face: "E", look: "egypt.gallery.chest.look" },
    { id: "dinner", name: "bread and beer", rect: [283, 314, 47, 44], walkTo: [355, 380], face: "W", look: "egypt.gallery.dinner.look" },
    { id: "sledge-runner", name: "sledge runner", rect: [472, 299, 19, 113], walkTo: [460, 413], face: "E", look: "egypt.gallery.runner.look" },
    { id: "marks", name: "builders' marks", rect: [568, 322, 61, 117], walkTo: [501, 538], face: "E", look: twice("egypt.gallery.marks.look", "egypt.gallery.marks.look2") },
    {
      id: "low-passage", name: "low passage", verb: "Look into", rect: [373, 376, 54, 63], walkTo: [400, 511], face: "N",
      look: "egypt.gallery.low.look", use: "egypt.gallery.low.use",
      useWith: { flashlight: (g) => g.say(g.flag("egypt.knowsLight") ? "egypt.flash.dead" : "egypt.gallery.low.flashlight") },
    },
    {
      id: "slot-foot", name: "slot in the bench", rect: [520, 398, 47, 57], walkTo: [462, 471], face: "E",
      look: (g) => g.say(g.flag("egypt.footSet") ? "egypt.gallery.slot.set" : g.flag("egypt.shadeSet") ? "egypt.gallery.slot.beam" : "egypt.gallery.slot.look"),
      useWith: { carmirror: wedgeMirror, coppermirror: "egypt.foot.wrong", shade: "egypt.gallery.shade" },
    },
    { id: "oil-jars", name: "oil jars", verb: "Borrow", rect: [216, 431, 109, 89], walkTo: [316, 529], face: "W", look: "egypt.gallery.jars.look", use: "egypt.gallery.jars.use" },
    { id: "rope", name: "coil of rope", rect: [487, 500, 47, 23], walkTo: [475, 527], face: "E", look: "egypt.gallery.rope.look" },
    {
      id: "way-out", name: "way out", verb: "Take the", poly: [[164, 593], [222, 511], [221, 389], [164, 431]], walkTo: [239, 542], face: "W",
      look: "egypt.gallery.out.look", use: (g) => g.goto("egypt-site", { spawn: g.flag("egypt.cameDown") ? "fromGalleryAgain" : "fromGallery" }),      // (the long stair outside is walked whole only once)
    },
    { id: "ladder", name: "ladder", rect: [92, 250, 66, 350], walkTo: [210, 569], face: "W", look: "egypt.gallery.ladder.look" },
    {
      id: "lampboy", name: "lamp boy", verb: "Talk to", rect: [548, 470, 60, 112], walkTo: [510, 572], face: "E",
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

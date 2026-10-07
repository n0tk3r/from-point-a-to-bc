// Act One, the last of four scenes: the burial chamber.
// Egypt, about 2560 B.C. Dad plays.
//
// Red granite, no pictures, and the king's furniture half unpacked. The old goldsmith works on by lamplight:
// he is too deaf to hear the hum, and mishears everything else. The door in time is here, in the bare wall
// by the sarcophagus. It is shut, it cannot be seen, and it hums.
//
//   chain B    The flashlight, shone at the place that hums, opens a hole the size of a dinner plate. Then the
//              batteries die, and Dad says the rule out loud: light opens it, and more light, more door.
//              (This sets "egypt.knowsLight", which is what lets him take the shade and the mirror off the wagon.)
//   chain C3   The goldsmith's eyes are tired of shining things. The sunglasses buy his copper hand mirror.
//   the gate   With the shade up outside and both mirrors in the gallery, the sunbeam comes in at the doorway
//              and lands on the wall, and the door opens wide. Dad steps up to it, and the act ends.
//
// The door and every beam are light, so they are drawn live. Nothing of the door shows until it is opened.
//
// Try it: index.html?scene=egypt-chamber&lead=dad
// Later states: &flags=egypt.arrived,egypt.inside,egypt.sawChamber,egypt.knowsLight,egypt.shadeSet,egypt.footSet,egypt.topSet

const art = "art/scenes/egypt-chamber/";

/** How many times a line has been spoken. (The engine counts every line it says.) */
const count = (g, id) => g.store.data.seenLines[id] || 0;
/** A thing worth looking at twice: the first line, then the second, turn about. */
const twice = (first, second) => (g) => g.say(count(g, first) <= count(g, second) ? first : second);
/** Is the sunbeam complete: shade outside, door mirror at the foot of the gallery, copper mirror at the top? */
const allSet = (g) => !!(g.flag("egypt.shadeSet") && g.flag("egypt.footSet") && g.flag("egypt.topSet"));
/** Dad keeps his arm out, as at the top of a reach, until told to drop it: he is holding something up. */
const holdOut = (g, on) => { if (g.lead) g.lead.hold(on); };

// ---------- light: the door, the sunbeam, the flashlight, the lamps ----------
// The place that hums is a door-sized piece of bare wall between the king's furniture and the sarcophagus, from
// x 462 to 542, and the air in front of it. The kit draws a door in time as a round thing; the scripts squeeze it to fit.
const DOOR = [500, 338, 96];                                          // the middle of the open door, and half its height: it stands from y 242 down to the floor
const WIDE = 0.48;                                                    // wide open it is an oval, this much as wide as it is high (92 by 192)
const PLATE = 0.11;                                                   // the hole a flashlight opens, beside the whole door: round, the size of a dinner plate
const HOLE = [28, 18];                                                // where that hole opens, from the middle of the door: in the air at (528, 356), just past his hand
const BEAM = [[98, 380], [104, 404], [502, 310], [498, 290]];         // the soft outer light of the sunbeam: from the middle of the doorway (101, 392) across to the wall (500, 300)
const CORE = [[100, 388], [102, 396], [501, 304], [499, 296]];        // its bright middle
const FLASH_FAR = [[505, 397], [511, 399], [538, 361], [518, 351]];   // the flashlight's light, from his hand to the hole, where he first stands
const FLASH_NEAR = [[521, 375], [527, 377], [537, 360], [520, 352]];  // and from a step nearer
const LAMPS = [[160, 278, 0.8], [371, 283, 0.8], [256, 429, 0.9], [706, 374, 0.8], [775, 448, 1], [58, 494, 1]];   // each flame, and how big things are there
const points = (shape) => shape.map((p) => p.join(",")).join(" ");
/** Show or hide a part of the light at once (setup), or bring it up over a moment (scripts). */
const lit = (g, id, on) => { const el = g.q("#" + id); if (el) el.setAttribute("opacity", on ? 1 : 0); };
const glow = (g, id, ms = 900) => { const el = g.q("#" + id); return el ? g.tween(ms, (k) => el.setAttribute("opacity", k)) : Promise.resolve(); };

/** Dress the door. `high` is how much of its full height it has (0 is shut and unseen, 1 is wide open); `wide` is its
    width beside that height (1 for a round hole); `at` moves its middle (the flashlight's hole is off to one side). */
function door(g, high, wide = 1, flicker = false, at = [0, 0]) {
  const whole = g.q("#door"), hole = g.q("#hole");
  if (!whole || !hole) return;
  whole.style.display = high > 0 ? "" : "none";
  hole.style.transform = `translate(${at[0]}px, ${at[1]}px) scale(${Math.max(high * wide, 0.01)}, ${Math.max(high, 0.01)})`;
  hole.classList.toggle("flicker", flicker);
}

/** Draw someone as another figure from js/art/people.js (the same man, dressed differently), keeping his id, his
    place and the way he faces. If that figure has not been drawn yet, he stays as he is. */
function redraw(g, id, kind) {
  const cast = g.view.cast, old = g.actor(id);
  if (!old || old.kind === kind) return;
  cast.remove(id);
  try { cast.addFigure(id, kind, old.x, old.y, old.scale).face(old.yaw); }
  catch { cast.add(old); }
}

/** Make the picture match the story facts: the door and the sunbeam are there once the door has opened wide, and
    not before; the goldsmith wears the sunglasses once they are his. */
function dress(g) {
  const open = !!g.flag("egypt.doorOpen");
  lit(g, "beam", open);
  lit(g, "flash", false);
  door(g, open ? 1 : 0, WIDE);
  if (g.flag("egypt.hasCopper")) redraw(g, "goldsmith", "goldsmith-shades");
}

// ---------- chain B: the flashlight ----------
async function shine(g) {
  if (g.flag("egypt.knowsLight")) return g.say("egypt.flash.dead");
  const cone = g.q("#flash"), ray = g.q("#flash-ray");
  await g.say(g.flag("egypt.heardBoy") ? "egypt.flash.1" : "egypt.flash.1b");
  await g.reach();
  try {
    holdOut(g, true);                                                              // the flashlight, pointed at the place that hums
    if (ray) ray.setAttribute("points", points(FLASH_FAR));
    if (cone) cone.setAttribute("opacity", 1);
    await g.wait(350);
    g.sfx("portal");
    await g.tween(700, (k) => door(g, PLATE * k, 1, true, HOLE), g.ease.out);     // a hole in the air, the size of a dinner plate
    await g.say("egypt.hole.look");
    holdOut(g, false);
    await g.walkTo(470, 480);                                                      // he steps nearer...
    g.lead.face("NE");
    holdOut(g, true);
    if (ray) ray.setAttribute("points", points(FLASH_NEAR));
    await g.tween(500, (k) => door(g, PLATE * (1 - 0.45 * k), 1, true, HOLE));     // ...and it shrinks
    await g.say("egypt.hole.small");
    for (const level of [0.3, 1, 0.2, 0.7, 0]) {                                   // the batteries give out
      if (cone) cone.setAttribute("opacity", level);
      await g.wait(130);
    }
    await g.tween(350, (k) => door(g, PLATE * 0.55 * (1 - k), 1, true, HOLE));     // and the hole goes with them
  } finally {                                                                      // whatever happens, nothing of it is left on the stage
    door(g, 0);
    lit(g, "flash", false);
    holdOut(g, false);
  }
  await g.say("egypt.flash.dies");
  if (!g.flag("egypt.heardBoy")) await g.say("egypt.flash.son");                   // he has worked out for himself what the lamp boy would have told him
  await g.say("egypt.flash.rule.1", "egypt.flash.rule.2");
  g.flag("egypt.knowsLight", true);
  g.flag("egypt.heardBoy", true);                 // (so the Hint button does not send him to hear what he now knows)
  await g.say("egypt.goldsmith.flash");
}

// ---------- chain C3: the goldsmith, his eyes, his mirror ----------
async function talkToGoldsmith(g) {
  if (!g.flag("egypt.metGoldsmith")) {
    await g.say("egypt.goldsmith.meet.1", "egypt.goldsmith.meet.2", "egypt.goldsmith.meet.3");
    g.flag("egypt.metGoldsmith", true);
  }
  for (;;) {
    const pick = await g.choose([
      { id: "boy", line: "egypt.ask.boy" },
      { id: "hum", line: "egypt.goldsmith.ask.hum" },
      { id: "eyes", line: "egypt.goldsmith.ask.eyes" },
      { id: "king", line: "egypt.goldsmith.ask.king" },
      { id: "bye", line: "egypt.goldsmith.ask.bye" },
    ]);
    if (pick === "boy") await g.say("egypt.ask.boy", "egypt.goldsmith.boy.1", "egypt.goldsmith.boy.2", "egypt.goldsmith.boy.3");
    else if (pick === "hum") await g.say("egypt.goldsmith.ask.hum", "egypt.goldsmith.hum.1", "egypt.goldsmith.hum.2");
    else if (pick === "eyes") {
      if (g.flag("egypt.hasCopper")) await g.say("egypt.goldsmith.ask.eyes", "egypt.goldsmith.eyes.after");
      else await g.say("egypt.goldsmith.ask.eyes", "egypt.goldsmith.eyes.1", "egypt.goldsmith.eyes.2", "egypt.goldsmith.eyes.3");
    }
    else if (pick === "king") await g.say("egypt.goldsmith.ask.king", "egypt.goldsmith.king.1", "egypt.goldsmith.king.2");
    else return g.say("egypt.goldsmith.ask.bye", "egypt.goldsmith.bye");
  }
}

/** The sunglasses for the mirror. Kindness is not kept waiting: this works whether or not Dad knows yet what a mirror is for. */
async function trade(g) {
  await g.say("egypt.goldsmith.trade.1", "egypt.goldsmith.trade.2");
  await g.reach();
  g.take("sunglasses");
  redraw(g, "goldsmith", "goldsmith-shades");     // he puts them on
  await g.say("egypt.goldsmith.trade.3", "egypt.goldsmith.trade.4");
  await g.reach();
  g.flag("egypt.hasCopper", true);                // the mirror leaves the bench (its cut-out and its clickable area follow the fact)
  g.give("coppermirror");
  await g.say("egypt.goldsmith.trade.5");
  if (!g.flag("egypt.knowsLight")) await g.say("egypt.goldsmith.trade.early");
}

// ---------- the gate ----------
/** The sunbeam arrives, and the door opens wide. Played once, the first time he comes in with all three reflectors in place. */
async function sunrise(g) {
  await g.walkTo(214, 524);                       // he steps out of the doorway, out of the sunbeam's way
  g.lead.face("E");
  await g.wait(300);
  await glow(g, "beam", 1200);
  await g.say("egypt.gate.1");
  g.sfx("portal");
  await g.tween(1600, (k) => door(g, k, 1 - (1 - WIDE) * k), g.ease.out);      // it opens round, and stretches to a doorway as it grows
  g.flag("egypt.doorOpen", true);
  await g.say("egypt.hole.big", "egypt.gate.gold");
}

async function useDoor(g) {
  if (g.flag("egypt.ready")) return g.say("egypt.hole.wait");
  await g.say("egypt.hole.go");
  g.flag("egypt.ready", true);
  // Act break: leave Dad at the door and pick the story up with the Son, in Rome.
  const d = g.store.data;
  g.rememberPlace();
  d.act = 2;
  d.active = "son";
  await g.fade(1, 500);
  await g.card("Meanwhile", "about twenty-five hundred years later", { plain: true });
  await g.goto("rome-steps", { via: "wormhole" });
}

export default {
  id: "egypt-chamber",
  era: "egypt",
  name: "The burial chamber",

  // Every number below is a pixel of the painting, measured by the painter (art/scenes/egypt-chamber/layout.json).
  // DEPTH: a room, so people shrink only a little toward the back wall.
  horizon: -200, full: 585,

  // The granite floor, less the king's furniture along the back wall and the sarcophagus on the right. In front of
  // the place that hums the floor runs right up to the wall.
  walk: { area: [[86, 470], [120, 461], [160, 467], [456, 467], [465, 440], [546, 440], [550, 509], [752, 509], [757, 529], [792, 529], [792, 594], [150, 594], [72, 584], [72, 498]] },
  spawn: {
    default: [150, 484],
    fromGallery: [150, 484],        // in at the low doorway on the left
  },
  exits: ["egypt-gallery", "rome-steps"],

  picture: art + "back.png",

  // The goldsmith sits BEHIND his bench: his feet are above its base row, so the bench and what is on it lie over his knees.
  planes: [
    { id: "bench", src: art + "bench.png", base: 512, solid: [[185, 517], [417, 512], [417, 498], [356, 494], [251, 494], [189, 505]] },      // the bench, his jug and his brazier
    { id: "mirror", src: art + "mirror.png", base: 513, when: (g) => !g.flag("egypt.hasCopper") },                                         // propped on the bench, until he trades it away
    { id: "front", src: art + "front.png", plane: "front" },
  ],

  // Everything here is light. The sunbeam, the flashlight and the door all start hidden: dress() shows what the
  // facts say, and the scripts above play the moments in between. Nothing of the door is drawn until it is opened.
  live(kit) {
    const flame = ([x, y, k], n) => `<ellipse cx="${x}" cy="${y - 2 * k}" rx="${9 * k}" ry="${11 * k}" fill="#ffc266" opacity="0.5" filter="url(#lamp-soft)"/>` +
      `<ellipse class="flicker" cx="${x}" cy="${y - 3 * k}" rx="${5 * k}" ry="${7 * k}" fill="#ffe9b0" opacity="0.8" filter="url(#lamp-soft)" style="animation-delay:${-0.41 * n}s"/>`;
    return `<defs><filter id="sun-soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
        <filter id="sun-edge" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.6"/></filter>
        <filter id="lamp-soft" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="2.5"/></filter></defs>
      <g shape-rendering="geometricPrecision">${LAMPS.map(flame).join("")}</g>
      <g id="beam" opacity="0" shape-rendering="geometricPrecision">
        <polygon points="${points(BEAM)}" fill="#ffe7a0" opacity="0.3" filter="url(#sun-soft)"/>
        <polygon points="${points(CORE)}" fill="#fff4c8" opacity="0.55" filter="url(#sun-edge)"/>
        <ellipse cx="500" cy="300" rx="30" ry="38" fill="#fff3c4" opacity="0.55" filter="url(#sun-soft)"/>
      </g>
      <g id="flash" opacity="0" shape-rendering="geometricPrecision">
        <polygon id="flash-ray" points="${points(FLASH_FAR)}" fill="#f4f8ff" opacity="0.3" filter="url(#sun-soft)"/>
        <ellipse cx="${DOOR[0] + HOLE[0]}" cy="${DOOR[1] + HOLE[1]}" rx="18" ry="18" fill="#f4f8ff" opacity="0.5" filter="url(#sun-soft)"/>
      </g>
      <g id="door" style="display:none">${kit.portal(DOOR[0], DOOR[1], DOOR[2], "hole")}</g>`;
  },

  actors: [
    { id: "goldsmith", kind: "goldsmith", at: [330, 494], face: "SE" },       // on his stool, behind the bench
  ],

  setup: dress,

  // The far things first: an area lower in this list lies over the ones above it.
  hotspots: [
    { id: "walls", name: "granite walls", rect: [140, 20, 620, 166], look: twice("egypt.chamber.walls.look", "egypt.chamber.walls.look2") },
    {
      id: "doorway", name: "doorway", verb: "Go through", poly: [[135, 330], [135, 413], [67, 469], [67, 369]], walkTo: [106, 468], face: "W",
      look: "egypt.chamber.door.look", use: (g) => g.goto("egypt-gallery", { spawn: "fromChamber" }),
    },
    { id: "treasure", name: "the king's furniture", verb: "Touch", rect: [138, 186, 322, 282], walkTo: [392, 478], face: "N", look: twice("egypt.chamber.treasure.look", "egypt.chamber.treasure.look2"), use: "egypt.chamber.treasure.use" },
    { id: "lid", name: "sarcophagus lid", rect: [588, 328, 164, 56], walkTo: [700, 532], face: "N", look: "egypt.chamber.lid.look" },
    {
      id: "sarcophagus", name: "sarcophagus", verb: "Climb into", poly: [[560, 500], [746, 500], [746, 415], [731, 383], [554, 383], [560, 415]], walkTo: [650, 532], face: "N",
      look: twice("egypt.chamber.sarc.look", "egypt.chamber.sarc.look2"), use: "egypt.chamber.sarc.use",
    },
    {
      id: "hum", name: "wall that hums", verb: "Touch", rect: [462, 236, 80, 164], walkTo: [452, 506], face: "NE", when: (g) => !g.flag("egypt.doorOpen"),
      look: (g) => g.say(g.flag("egypt.knowsLight") ? "egypt.hum.look2" : "egypt.hum.look"),
      use: (g) => g.say(g.flag("egypt.knowsLight") ? "egypt.hum.use2" : "egypt.hum.use"),
      useWith: { flashlight: shine, carmirror: "egypt.hum.mirror", coppermirror: "egypt.hum.mirror", shade: "egypt.hum.shade" },
    },
    {
      id: "door", name: "humming door", verb: "Go through", walkTo: [500, 500], face: "N", when: (g) => !!g.flag("egypt.doorOpen"),
      poly: [[546, 338], [540, 386], [523, 421], [500, 434], [477, 421], [460, 386], [454, 338], [460, 290], [477, 255], [500, 242], [523, 255], [540, 290]],
      look: "egypt.hole.big", use: useDoor,
      useWith: { flashlight: "egypt.flash.dead" },
    },
    { id: "bench", name: "goldsmith's bench", rect: [192, 426, 162, 96], walkTo: [300, 528], face: "N", look: "egypt.chamber.bench.look" },
    { id: "brazier", name: "brazier", rect: [356, 478, 54, 38], walkTo: [434, 524], face: "W", look: "egypt.chamber.brazier.look" },
    {
      id: "goldsmith", name: "goldsmith", verb: "Talk to", rect: [302, 384, 60, 80], walkTo: [434, 524], face: "NW",
      look: (g) => g.say(g.flag("egypt.hasCopper") ? "egypt.goldsmith.look2" : "egypt.goldsmith.look"), use: talkToGoldsmith,
      useWith: {
        sunglasses: trade, rootbeer: "egypt.goldsmith.rootbeer", pass: "egypt.goldsmith.pass", carmirror: "egypt.goldsmith.carmirror", coppermirror: "egypt.goldsmith.copper",
        flashlight: (g) => g.say(g.flag("egypt.knowsLight") ? "egypt.flash.dead" : "egypt.goldsmith.flashlight"),
      },
    },
    {
      id: "mirror", name: "copper mirror", verb: "Borrow", rect: [289, 440, 29, 40], walkTo: [304, 528], face: "N", when: (g) => !g.flag("egypt.hasCopper"),
      look: "egypt.chamber.mirror.look", use: ["egypt.chamber.mirror.use", "egypt.goldsmith.mirror.no"],
    },
  ],

  // Runs when the lead arrives. It must be safe to run twice, so each part checks its own fact.
  async enter(g) {
    if (!g.flag("egypt.sawChamber")) {
      await g.wait(400);
      await g.say("egypt.chamber.arrive.1", "egypt.chamber.arrive.2");
      g.flag("egypt.sawChamber", true);
    }
    if (allSet(g) && !g.flag("egypt.doorOpen")) await sunrise(g);
  },
};

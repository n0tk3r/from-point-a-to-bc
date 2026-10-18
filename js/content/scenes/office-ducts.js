// Act Five, continued: the Office's air ducts (SCENES-17: new in round seventeen; briefs/SCENES-17.md, and the design,
// briefs/out/office-hq-design.md, section 4, "The ducts"). A long sheet-metal run over the ground floor at Ranger's
// height, lit from below by the grilles of the rooms it passes over: ROOM C (the Comfortable Room), PROP & EFF, BREAK and
// HALL; the intake up to the roof at the left, and at the right the B-7 shaft, its big fan stopped (the fans are off before
// Ranger is ever in here: #16). Nobody but Ranger is ever here.
//
// From each grille he looks down into the room under it (js/engine/grille.js: the room as it is, its people living their
// lives, seen through the slats; only what answers from above, `peek`, is there to click), and where there is something to
// land on and nobody looking he drops into it, and climbs back up the way he came:
//   ROOM C      onto the spare chair's seat, once the suits have gone and Grandpa Joe is not standing on it
//   PROP & EFF  onto the top shelf, under the grille (Opal's back is to the shelves)
//   BREAK       onto the fridge (with Jed there, Jed shoos him back up: the break room's `enter`)
//   HALL        there is no painting of the hall in stage one: the grille is an area of its own (the elevator, its
//               arrow pointing down; nothing to land on), and "Going Down" shows the hall through it
// The vent between him and Grandpa Joe is the grille over ROOM C: a thing used on it is handed down (the scene below
// plays it: office-room.js), and he hears Joe through it once the suits have gone.
//
// Every place is the painter's own measurement of the finished picture (art/scenes/office-ducts/layout.json, PAINT-17B's
// ready.md). The ducts are being painted again (PAINT-17B2) so that they read better as a duct: the camera, the walk band,
// the marks, the four grilles and the B-7 fan's cut-out stay exactly as they are, and every other thing may move. Their
// shapes are in ONE block below (SHAPES), written from layout.json by briefs-out/office-ducts-shapes.py: run it again on
// the new layout.json and the block follows it (office-check.mjs says whether the block and the layout agree).
//
// Try it: index.html?scene=office-ducts&lead=ranger&flags=office.arrived,office.inside,office.acOff

import { STOCK, ANNOUNCE, BUILDING, WORDS, is, heard, keepHeat, shades, onChair, think } from "./office-common.js";

const art = "art/scenes/office-ducts/";

// ---------- the marks (layout.json marks: all on row 470, all facing E) ----------
const MARKS = { intake: [71, 470], "over-room": [175, 470], "over-property": [295, 470], "over-break": [415, 470], "over-hall": [535, 470], shaft: [618, 470] };
// The four grilles in the duct's floor (layout.json things grille-*: these stay exactly), and where each one is in the
// picture of the room below (the drop falls from there: PAINT-17C's and PAINT-17D's `vent.grille`).
const GRILLE = {
  room: [[193, 397], [253, 397], [253, 526], [193, 526]],
  property: [[320, 397], [367, 397], [367, 526], [320, 526]],
  break: [[442, 397], [490, 397], [490, 526], [442, 526]],
  hall: [[556, 397], [617, 397], [617, 526], [556, 526]],
};
const FROM = { room: [106, 201], property: [155, 142], break: [202, 133] };

// ==== BEGIN LAYOUT SHAPES (office-ducts): written by briefs-out/office-ducts-shapes.py from the painter's layout.json; do not edit by hand.
// Every thing of the ducts that the painting may move (all but the grilles, the marks and the B-7 fan's cut-out): its
// area (rect, poly or circle), where Ranger stands to it and which way he faces. MERGE-17: run the script again after
// the ducts are painted again, and this block follows the new layout.json in one step.
const SHAPES = {
  "intake": {"poly": [[0, 78], [130, 78], [130, 436], [0, 436]], "stand": [71, 470], "face": "E"},
  "shaft": {"poly": [[595, 78], [799, 78], [799, 599], [644, 599], [644, 481], [619, 481], [619, 353], [644, 353], [644, 341], [595, 341]], "stand": [618, 470], "face": "E"},
  "stencil": {"poly": [[622, 356], [736, 356], [736, 418], [622, 418]], "stand": [618, 470], "face": "E"},
  "fan": {"poly": [[652, 525], [753, 525], [753, 576], [652, 576]], "stand": [618, 470], "face": "E"},
  "pipe": {"poly": [[165, 287], [194, 287], [218, 287], [242, 287], [266, 286], [290, 287], [314, 287], [338, 287], [362, 287], [386, 287], [410, 287], [434, 286], [458, 287], [482, 286], [506, 287], [530, 287], [554, 287], [578, 287], [599, 287], [599, 304], [578, 304], [554, 304], [530, 304], [506, 304], [482, 304], [458, 304], [434, 304], [410, 304], [386, 304], [362, 304], [338, 304], [314, 304], [290, 304], [266, 304], [242, 304], [218, 304], [194, 304], [165, 304]], "stand": [400, 470], "face": "N"},
  "valve": {"rect": [428, 288, 14, 14], "stand": [435, 470], "face": "N"},
  "wires": {"poly": [[166, 230], [186, 230], [202, 229], [218, 227], [234, 227], [250, 229], [266, 230], [282, 230], [298, 229], [314, 227], [330, 227], [346, 229], [362, 230], [378, 230], [394, 229], [410, 227], [426, 227], [442, 229], [458, 230], [474, 230], [490, 229], [506, 229], [522, 227], [538, 228], [554, 230], [570, 230], [586, 230], [598, 230], [598, 242], [586, 242], [570, 243], [554, 242], [538, 241], [522, 241], [506, 242], [490, 242], [474, 243], [458, 243], [442, 242], [426, 241], [410, 241], [394, 242], [378, 243], [362, 243], [346, 242], [330, 241], [314, 241], [298, 242], [282, 243], [266, 243], [250, 242], [234, 241], [218, 241], [202, 242], [186, 242], [166, 243]], "stand": [380, 470], "face": "N"},
  "insulation": {"rect": [125, 318, 521, 25], "stand": [400, 470], "face": "N"},
  "cup": {"rect": [285, 503, 19, 17], "stand": [294, 470], "face": "S"},
  "pencil": {"rect": [492, 513, 23, 10], "stand": [504, 470], "face": "S"},
  "wrapper": {"rect": [520, 510, 23, 12], "stand": [532, 470], "face": "S"},
  "fitting": {"rect": [94, 490, 98, 39], "stand": [143, 470], "face": "S"},
  "bulb": {"rect": [691, 308, 17, 18], "stand": [627, 470], "face": "N"},
  "lifted": {"rect": [489, 494, 57, 17], "stand": [518, 470], "face": "S"},
  "intakefan": {"rect": [6, 81, 112, 50], "stand": [71, 470], "face": "E"},
  "rivets": {"rect": [286, 351, 14, 108], "stand": [293, 470], "face": "N"},
  "tiles": {"poly": [[0, 494], [643, 494], [643, 528], [0, 528]], "stand": [330, 470], "face": "S"},
};
// ==== END LAYOUT SHAPES

/** A thing's area from its shape in SHAPES: { rect }, { poly } or { circle }. */
const area = (s) => (s.rect ? { rect: s.rect } : s.circle ? { circle: s.circle } : { poly: s.poly });
/** One of the ducts' things: its area, where Ranger stands to it, and his look and use (thoughts). */
const thing = (id, name, look, use, more = {}) => ({ id, name, ...area(SHAPES[id]), walkTo: [Math.min(618, Math.max(71, SHAPES[id].stand[0])), 470],
  face: SHAPES[id].face === "N" || SHAPES[id].face === "S" ? SHAPES[id].face : "E", look: { ranger: look }, use: { ranger: use }, ...more });

// ---------- the grilles ----------
/** ROOM C: a voice he knows, under the questions; once he has looked down, Joe; and with the suits gone, Joe hears him. */
const roomLook = Object.assign(async (g) => think(g, is(g, "office.sawRoom") ? "office.duct.room.found.ranger" : "office.duct.room.ranger", "office.duct.room.ranger.joe"),
  { lines: ["office.duct.room.ranger", "office.duct.room.found.ranger", "office.duct.room.ranger.joe"] });
/** May he drop into the Comfortable Room? The suits gone, and nobody standing on the chair he lands on. */
const roomDrop = (g) => is(g, "office.alone") && !onChair(g);
const roomNo = (g) => g.say(is(g, "office.alone") ? "office.duct.drop.no.ranger" : "office.duct.drop.suits.ranger");
/** HALL: no painting of the hall in stage one. Looked down through, the elevator (the first time); then, would he drop?
    Nothing to land on; and after that, nothing doing. */
async function hall(g) {
  const r = g.lead;
  if (r && r.play && !g.clock.skipping) await r.play(g.clock, "peek", { ms: 900 });
  if (!is(g, "office.sawHall")) { g.flag("office.sawHall", true); return g.say("office.duct.hall.first.ranger"); }
  if (!heard(g, "office.duct.drop.hall.ranger")) return g.say("office.duct.drop.hall.ranger");
  return g.say("office.duct.hall.use.ranger");
}
/** A thing used on a grille: handed down through it. The room below plays it (its own areas' `peek` `useWith`), so he looks
    down first, and the thing goes down in the view. Anything else: he keeps it. */
const handVia = (spot, item) => async (g) => {
  if (!(await g.lookDown(spot))) return;
  if (g.peeking && typeof g.scene.handDown === "function") await g.scene.handDown(g, item);      // (office-room.js, office-property.js)
};
const DOWN_ROOM = ["pietin", "peanuts", "schedule", "bottlecap", "receipt"];

// ---------- the B-7 shaft ----------
/** Down the shaft? Not without Joe (WRITE-17's line for the whole stage; B-7's own refusal, [down, no], is the map's:
    js/content/maps.js, the landmark b7). */
const shaftUse = (g) => g.say("office.duct.shaft.use.ranger");

export default {
  id: "office-ducts",
  era: "nevada",
  name: "The Office: the ducts",
  building: BUILDING,
  music: "office",

  // DEPTH (layout.json): Ranger walks the middle of the duct's floor on row 470, held at exactly his painted size.
  horizon: 333, full: 470, minScale: 1.0, maxScale: 1.0,
  walk: { area: [[62, 466], [623, 466], [638, 475], [39, 475]] },

  spawn: { default: MARKS.intake, ...MARKS },
  facing: "E",
  exits: ["office-lot", "office-room", "office-property", "office-breakroom"],
  stock: STOCK,
  announce: ANNOUNCE,
  // Words of someone not on the stage (Grandpa Joe, heard through the grille over his room): up through ROOM C's slats.
  get wordsAt() { return WORDS.at || [225, 525]; },
  tick(g) { keepHeat(g); },

  picture: art + "back.png",
  planes: [
    // the B-7 fan across the shaft: turning while the building's air is on, stopped once the switch is pulled (#16)
    { id: "fan", frames: [0, 1, 2, 3].map((n) => art + `fan-${n}.png`), fps: 3, at: [693, 550], foot: [39, 23], base: 573, when: (g) => !is(g, "office.acOff") },
    { id: "fan-stopped", src: art + "fan-stopped.png", at: [693, 550], foot: [39, 23], base: 573, when: (g) => is(g, "office.acOff") },
  ],

  // Back to front: the big things first (the shaft, the insulation, the intake), then the smaller ones over them, and the
  // grilles last (over the ceiling tiles round them).
  hotspots: [
    thing("shaft", "B-7 shaft", "office.duct.shaft.ranger", shaftUse),
    thing("tiles", "ceiling tiles", "office.duct.tiles.ranger", "office.duct.tiles.ranger"),
    thing("insulation", "insulation", "office.duct.insulation.ranger", "office.duct.insulation.use.ranger"),
    thing("rivets", "rivets", "office.duct.rivets.ranger", "office.duct.rivets.use.ranger"),
    thing("pipe", "water pipe", "office.duct.pipe.ranger", "office.duct.pipe.use.ranger"),
    thing("valve", "valve", "office.duct.pipe.ranger", "office.duct.pipe.use.ranger"),
    thing("wires", "wires", "office.duct.wires.ranger", "office.duct.wires.use.ranger"),
    thing("stencil", "stencil", "office.duct.stencil.ranger", "office.duct.stencil.use.ranger"),
    thing("fan", "big fan", "office.duct.fan.ranger", "office.duct.fan.use.ranger"),
    thing("bulb", "light", "office.duct.light.ranger", "office.duct.light.use.ranger"),
    thing("fitting", "light fitting", "office.duct.light.ranger", "office.duct.light.use.ranger"),
    thing("lifted", "ceiling tile", "office.duct.tiles.ranger", "office.duct.tiles.ranger"),
    thing("cup", "coffee cup", "office.duct.cup.ranger", "office.duct.cup.use.ranger"),
    thing("pencil", "pencil", "office.duct.pencil.ranger", "office.duct.pencil.use.ranger"),
    thing("wrapper", "sandwich wrapper", "office.duct.wrapper.ranger", "office.duct.wrapper.use.ranger"),
    // the intake: the way back up to the roof (a climb: out at the lot's `intake`, in front of the unit's open grille)
    thing("intake", "intake", "office.duct.intake.ranger", "office.duct.intake.ranger",
      { verb: "Climb up", climb: { scene: "office-lot", spawn: "intake", to: [66, 140], who: "ranger" } }),
    thing("intakefan", "intake fan", "office.duct.intakefan.ranger", "office.duct.intakefan.ranger"),
    // the four grilles (they stay exactly: the scenes below have their pictures of them)
    { id: "grille-room", name: "grille (ROOM C)", poly: GRILLE.room, walkTo: MARKS["over-room"], face: "E", look: { ranger: roomLook },
      grille: { scene: "office-room", spawn: "vent", from: FROM.room, when: roomDrop, no: roomNo },
      useWith: Object.fromEntries(DOWN_ROOM.map((item) => [item, handVia("grille-room", item)])) },
    { id: "grille-property", name: "grille (PROP & EFF)", poly: GRILLE.property, walkTo: MARKS["over-property"], face: "E",
      look: { ranger: "office.duct.prop.ranger" },
      grille: { scene: "office-property", spawn: "vent", from: FROM.property },
      useWith: Object.fromEntries(DOWN_ROOM.map((item) => [item, handVia("grille-property", item)])) },      // (the receipt goes; the rest: office.prop.with.ranger)
    { id: "grille-break", name: "grille (BREAK)", poly: GRILLE.break, walkTo: MARKS["over-break"], face: "E",
      look: { ranger: "office.duct.break.ranger" },
      grille: { scene: "office-breakroom", spawn: "fridge", from: FROM.break } },
    // HALL: no scene under it in stage one, so not a grille to the engine: its own use
    { id: "grille-hall", name: "grille (HALL)", verb: "Look down", poly: GRILLE.hall, walkTo: MARKS["over-hall"], face: "E",
      look: { ranger: "office.duct.hall.ranger" }, use: { ranger: hall } },
  ],

  setup(g) {
    keepHeat(g);
    shades(g);
  },

  async enter(g, from) {
    // just in at the intake, the first time: where's Joe?
    if (from === "office-lot" && g.store.data.active === "ranger" && !heard(g, "office.duct.in.ranger")) await g.say("office.duct.in.ranger");
  },
};

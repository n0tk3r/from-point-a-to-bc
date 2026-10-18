// ENGINE-17: the engine's own room under the sand: a sketch (no painting), for the proofs of round seventeen
// (js/content/scenes/engine-proof.js has the other half: the sand, with a grate in it). Not part of the story.
//
// It is the scene the proof's grate looks down into (docs/DESIGN.md, section 8, "Looking down through a grille"): seen from
// above, through the slats, its two people go on living and talk to each other when somebody looks in (`viewed`); its
// things answer from above as their `peek` says (the chest is looked at and used from above, the rug is a place to drop
// down onto, the table is looked at, anything else is not there to click from above); and from inside, the rope under the
// grate takes whoever dropped in back up (`climb`). It is in the same time as the sand (Egypt), on the same map (the
// proof's sand: a place of its own, "Under the sand"), so the critter down here and Dad up there are two leads in two
// scenes of one time: a thing is handed down through the grate and up again (g.pass, g.where), switching between them is
// their map with no Timer, and the map's travel is per lead (the critter is refused by this scene's `travel`, Dad by the
// place's: js/content/maps.js). It is in the proof's building, so the speakers are heard here (`building`).
//
// Try it: index.html?scene=engine-proof&lead=dad&flags=proof.grille (look down through the grate), or flags=proof.pass.

const LINES = {
  "proof.below.table.look": ["dad", "A table. Somebody down here eats standing up: there's no chair."],
  "proof.below.table.above": ["dad", "A table, from above. Breadcrumbs. They have bread down there and I don't."],
  "proof.below.table.drop": ["dad", "If I drop it on the table it'll roll off. It's that kind of table."],
  "proof.below.chest.look": ["dad", "A chest with a lid. Locked, of course. Chests always are."],
  "proof.below.chest.above": ["dad", "A chest, from above. You can see the dust on its lid from up here. Nobody's opened it in years."],
  "proof.below.chest.above.use": ["dad", "I could drop a pebble on it. That would be childish. ...It went 'tock'."],
  "proof.below.chest.use": ["dad", "Locked. Of course it is."],
  "proof.below.rug.look": ["dad", "A rug. Thick. A good thing to land on."],
  "proof.below.rug.above": ["dad", "A thick rug, right under the grate. Somebody planned for this."],
  "proof.below.rope.look": ["dad", "A rope, hanging from the grate. The way back up, if you have the arms for it."],
  "proof.below.grate.look": ["dad", "The grate I came down through. The sky's up there somewhere."],
  "proof.below.pacer.above": ["dad", "A man walking up and down down there, the way people do when they're waiting for news."],
  "proof.below.sitter.above": ["dad", "A man sitting on the floor with his tablet, writing everything down. Even me, probably."],
  "proof.below.pacer.look": ["dad", "He's pacing. Up and down. He's very good at it."],
  "proof.below.sitter.look": ["dad", "A scribe, writing. He hasn't looked up once."],
  "proof.below.talk.1": ["overseer", "Is somebody up there? I keep hearing feet on the sand."],
  "proof.below.talk.2": ["scribe", "It is the sand. Sand has feet. Write that down. ...I am writing it down."],
  "proof.below.critter.above": ["dad", "There he is, down there. He's looking up at me like I owe him something."],
  "proof.below.critter.look": ["dad", "The little bandit. He's made himself at home."],
  "proof.pass.down": ["dad", "Gum, coming down. Catch. ...Good catch."],
  "proof.pass.up": ["critter", "...", ["up", "hand"]],
  "proof.pass.up.dad": ["dad", "He's handing it back up. Through the grate. Generous little thing."],
  "proof.pass.nobody": ["critter", "...", ["up", "question"]],
  "proof.travel.critter": ["critter", "...", ["up", "no"]],
  "proof.travel.dad": ["dad", "Not by the map. The rope's the way up from down here."],
  "proof.below.arrive.dad": ["dad", "And down I go. Soft landing. Thank you, rug."],
};

const view = (g) => !!g.peeking;
/** From above: the gum dropped through the grate to the critter, if he is down here: handed across (g.pass), wherever Dad is. */
async function handDown(g) {
  const c = g.actor("critter");
  if (!c) return g.say("proof.below.table.drop");
  if (!g.pass("gum", "critter")) return;
  await g.arrive("gum", [400, -10], { to: [c.x + 14, c.y] });
  await g.say("proof.pass.down");
}
/** From down here, the gum handed up through the grate to Dad, if he is standing at it up there (his place: g.where). */
async function handUp(g) {
  const dad = g.where("dad");
  if (!dad || dad.scene !== "engine-proof" || dad.mark !== "grate") return g.say("proof.pass.nobody");
  if (g.lead) await g.reach();
  if (!g.pass("gum", "dad")) return;
  await g.say("proof.pass.up");
}

export default {
  id: "proof-below",
  era: "egypt",
  name: "Under the sand (a sketch)",
  building: "proof",                      // the proof's own building: g.pa is heard here (and on the sand, while proof.pa)
  horizon: 300, full: 590,
  walk: { area: [[90, 430], [710, 430], [780, 594], [20, 594]] },
  spawn: { default: [400, 540], vent: [400, 470], fromSand: [470, 520], critter: [560, 520] },
  // the map's travel, per lead: the critter may not leave from down here by the map (a thought: up, no); Dad's refusal is
  // the place's own (js/content/maps.js), so that both forms are shown
  travel: (g, who) => (who === "critter" ? "proof.travel.critter" : true),

  actors: [
    { id: "overseer", kind: "overseer", at: [240, 500], face: "E", life: { every: [10, 18], spots: [[170, 470, "W"], [300, 540, "E"]], stay: [2, 4] } },
    { id: "scribe", kind: "scribe", at: [640, 470], face: "W" },
  ],
  hotspots: [
    { id: "table", name: "table", rect: [120, 372, 130, 60], walkTo: [190, 462], face: "N", look: "proof.below.table.look",
      peek: { look: "proof.below.table.above", useWith: { gum: "proof.below.table.drop" } } },
    { id: "chest", name: "chest", rect: [590, 352, 110, 72], walkTo: [610, 452], face: "N", look: "proof.below.chest.look", use: "proof.below.chest.use",
      peek: { look: "proof.below.chest.above", use: "proof.below.chest.above.use" } },
    { id: "rug", name: "rug", poly: [[330, 474], [470, 474], [494, 518], [306, 518]], walkTo: [400, 500], look: "proof.below.rug.look",
      peek: { look: "proof.below.rug.above", drop: true } },
    { id: "rope", name: "rope", verb: "Climb", rect: [388, 300, 24, 150], walkTo: [400, 470], face: "N", look: "proof.below.rope.look",
      climb: { scene: "engine-proof", spawn: "grate", to: [400, 290] } },
    { id: "grate", name: "grate overhead", rect: [350, 268, 100, 30], walkTo: [400, 470], face: "N", look: "proof.below.grate.look",
      useWith: { gum: handUp } },
    { id: "overseer", name: "pacing man", rect: [222, 392, 40, 110], walkTo: [300, 520], look: "proof.below.pacer.look",
      peek: { look: "proof.below.pacer.above" } },
    { id: "scribe", name: "scribe", rect: [622, 428, 40, 46], walkTo: [600, 500], look: "proof.below.sitter.look",
      peek: { look: "proof.below.sitter.above" } },
    // the critter, when he is down here: from above, his own area (no shape: the box round his figure) answers from above
    { id: "critter-below", name: "small creature", mate: "critter", when: view, peek: { look: "proof.below.critter.above", useWith: { gum: handDown } } },
  ],

  setup(g) {
    for (const [id, line] of Object.entries(LINES)) if (!g.lines[id]) g.lines[id] = line;
  },
  /** Somebody looks in from above: the two of them talk, heard through the grate. */
  async viewed(g) {
    await g.say("proof.below.talk.1", "proof.below.talk.2");
  },
  async enter(g, from) {
    if (from === "engine-proof" && g.store.data.active === "dad" && !g.flag("proof.droppedIn")) {
      g.flag("proof.droppedIn", true);
      await g.say("proof.below.arrive.dad");
    }
  },
};

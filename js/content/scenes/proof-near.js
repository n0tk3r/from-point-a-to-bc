// ENGINE-21: not part of the story: the engine's own proof of a close-up scene (docs/DESIGN.md, section 8, "A close look that is
// a scene"), as Act Six's lock on the women's hall needs it: a strongbox's face seen close (art/proof/near.png), opened from the
// proof's sand (its strongbox: g.openCloseup), with nobody drawn in it and nobody walking; whoever is played is the one whose hand
// acts (each thing answers each lead in its own way); a hand drawn at each of its hand points while it is held (g.hand); two of
// its facts only for the moment (`momentary`: never saved, let go as it is left); "Step back" (the button, or Esc) back to the sand,
// everyone where they stood, and the scene hears it go (`leaving`). With the party (proof.party), Dad and the critter: a thing
// handed between them by a portrait here, where nobody has a box to click (ui.js reach).
// Three parts, each held while the next is done, as the lock's: the knob (anyone), the post (the critter's small hands: Dad's
// are too big), and then the slot opens the bolt. Try it: index.html?scene=engine-proof&lead=dad&flags=proof.near,proof.arrived

const LINES21N = {
  "proof.near.knob.look": ["dad", "A knob. It turns, and springs back when you let go."],
  "proof.near.knob.use": ["dad", "Holding it."],
  "proof.near.post.look": ["dad", "A square post. Something small could turn it."],
  "proof.near.post.dad": ["dad", "My fingers are too big for that."],
  "proof.near.post.first": ["dad", "It won't turn. Something else first."],
  "proof.near.post.use": ["critter", "...", ["hand", "up"]],
  "proof.near.slot.look": ["dad", "A slot. It wants everything else held first."],
  "proof.near.slot.notyet": ["dad", "Nothing. The other two first, both held."],
  "proof.near.slot.use": ["dad", "And it opens. Everybody let go."],
  "proof.near.bolt.look": ["dad", "The bolt. Shut, or not."],
  "proof.near.open": ["dad", "Open. The bolt's out."],
};

const held = (g, f) => !!g.flag(f);
/** Each hand where it is held: put back from the moment's facts whenever the scene is built (they are not saved). */
function hands(g) {
  g.hand("dad", held(g, "proof.knobHeld") ? "knob" : null, { from: "W" });
  g.hand("critter", held(g, "proof.postHeld") ? "post" : null, { from: "S", scale: 0.7 });
}
async function knob(g) {
  await g.say("proof.near.knob.use");
  g.flag("proof.knobHeld", true);
  hands(g);
}
async function post(g) {
  if (g.store.data.active !== "critter") return g.say("proof.near.post.dad");
  if (!held(g, "proof.knobHeld")) return g.say("proof.near.post.first");
  await g.say("proof.near.post.use");
  g.flag("proof.postHeld", true);
  hands(g);
}
async function slot(g) {
  if (!held(g, "proof.knobHeld") || !held(g, "proof.postHeld")) return g.say("proof.near.slot.notyet");
  g.sfx("chirp");
  g.flag("proof.latchOpen", true);
  await g.say("proof.near.slot.use");
  g.flag("proof.knobHeld", false); g.flag("proof.postHeld", false);
  hands(g);
}

export default {
  id: "proof-near",
  era: "egypt",
  name: "The strongbox, close",
  closeup: { back: "engine-proof", spawn: "default" },
  picture: "art/proof/near.png",
  party: (g) => (g.flag("proof.party") ? ["dad", "critter"] : null),
  hands: { knob: [322, 244], post: [400, 320], slot: [480, 220] },
  momentary: ["proof.knobHeld", "proof.postHeld"],
  hotspots: [
    { id: "knob", name: "knob", circle: [322, 244, 32], look: "proof.near.knob.look", use: knob },
    { id: "post", name: "square post", rect: [378, 298, 44, 44], look: "proof.near.post.look", use: post },
    { id: "slot", name: "slot", rect: [436, 204, 88, 32], look: "proof.near.slot.look", use: slot },
    { id: "bolt", name: "bolt", rect: [268, 376, 264, 28], look: (g) => g.say(g.flag("proof.latchOpen") ? "proof.near.open" : "proof.near.bolt.look") },
  ],
  setup(g) {
    for (const [id, line] of Object.entries(LINES21N)) if (!g.lines[id]) g.lines[id] = line;
    hands(g);
  },
  // the scene hears it as it is left ("Step back"): it lets go of everything (the moment's facts go by themselves: `momentary`)
  leaving(g) { g.flag("proof.letGo", true); },
};

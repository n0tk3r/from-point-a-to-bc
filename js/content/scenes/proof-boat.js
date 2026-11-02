// ENGINE-21: not part of the story: the engine's own proof of what Act Six's deck needs (briefs/out/edo2-design.md, section 9;
// docs/DESIGN.md, "Things that move by nature" and "The map, and the Timer"): a boat on the river by the proof's sand, a sketch
// with the engine's own cut-outs (art/proof/: tools/paint/proof_sea.py).
//   - AT SEA: on the proof's map ("proof-sand") this scene is a place that is a point of a way (`on`: half way along the way from
//     the sand round by the dunes): the map shows Dad's portrait there, on the way, and every place refuses with one line
//     (the place's `travel`: "proof.atsea").
//   - the ship's moving things: the far sea and its cape on a slow swell (`bob`, a pixel and a tilt), the sail breathing (`sway`
//     with anchor "belly"), the river's rows running past (`waves` with `run`), spray at the bow now and then (`spray` with
//     `every`), and a bucket of water thrown (`spray` on call: burst()).
// Try it: index.html?scene=proof-boat&lead=dad&flags=proof.arrived

const LINES21B = {
  "proof.atsea": ["dad", "We're on the river. The map can wait."],
  "proof.boat.sail.look": ["dad", "A sail, breathing. In, and out. In, and out."],
  "proof.boat.sea.look": ["dad", "The river going by in rows. We're moving. Or the river is."],
  "proof.boat.bucket.look": ["dad", "A bucket of river."],
  "proof.boat.bucket.use": ["dad", "Overboard it goes. Sorry, fish."],
};

/** A bucket of water thrown over the side: the splash (a spray of its own, on call), and its sound. */
async function throwBucket(g) {
  await g.say("proof.boat.bucket.use");
  g.sfx("splash");
  const s = g.effects.get("bucket");
  if (s) await s.burst();
  g.flag("proof.thrown", true);
}

export default {
  id: "proof-boat",
  era: "egypt",
  name: "On the river",
  horizon: 300, full: 590,
  walk: { area: [[60, 470], [740, 470], [760, 590], [40, 590]] },
  spawn: { default: [400, 540], deck: [400, 540], bow: [120, 520] },
  party: (g) => (g.flag("proof.party") ? ["dad", "critter"] : null),
  // the engine's own pictures (never keyed): the far sea with a cape (behind everybody), the sail above the deck
  planes: [
    { id: "far", src: "art/proof/far.png", plane: "back" },
    { id: "sail", src: "art/proof/sail.png", base: 330 },
  ],
  fx: [
    // the slow swell: the far sea and the cape a pixel up and down, tilting a quarter of a degree, on a long cycle
    { id: "swell", type: "bob", plane: "far", amount: 1, period: 9, tilt: 0.3 },
    // the sail breathing: its belly swelling out from the middle and easing, the yard and the foot still
    { id: "sail-breath", type: "sway", plane: "sail", anchor: "belly", amount: 2.4, period: 4.6, lean: 0.4 },
    // the river's rows running past, toward the stern (the boat goes to the left): the near rows faster
    { id: "rows", type: "waves", area: [[0, 238], [800, 238], [800, 300], [0, 300]], toward: "E", speed: 42, life: 2.4, run: true, rows: 6, per: 16 },
    // spray at the bow now and then (the boat meeting a wave), at the bow's row
    { id: "bow-spray", type: "spray", at: [70, 332], toward: [-50, -150], spread: 32, count: 16, every: [2.5, 5], life: 0.9, base: 340 },
    // a bucket of water thrown over the side, on call (the water men at Dōjima: `burst()` when the picture throws it)
    { id: "bucket", type: "spray", at: [640, 440], toward: [150, -110], spread: 22, count: 22, sheet: true, life: 0.8, gravity: 340, base: 450 },
  ],
  hotspots: [
    { id: "sail", name: "sail", poly: [[250, 62], [570, 62], [582, 330], [238, 330]], look: "proof.boat.sail.look" },
    { id: "sea", name: "river", rect: [0, 236, 800, 64], look: "proof.boat.sea.look" },
    { id: "bucket", name: "bucket", rect: [610, 430, 40, 40], walkTo: [600, 520], face: "E", look: "proof.boat.bucket.look", use: throwBucket },
  ],
  // the map's refusal (at sea) and the looks: the proof's own lines, added to the game's as the scene is built
  setup(g) { for (const [id, line] of Object.entries(LINES21B)) if (!g.lines[id]) g.lines[id] = line; },
};

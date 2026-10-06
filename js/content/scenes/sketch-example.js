// A scene with no drawing yet. Leave out `draw` and the engine sketches the place
// from its clickable areas: sky, ground, and a labelled box for each thing.
// That makes a scene playable as soon as its puzzle is written, so the story can
// be walked through and timed long before any art exists.
//
// Try it: index.html?scene=sketch-example&lead=son
// This scene is not part of the story. Delete it when you no longer need the example.

export default {
  id: "sketch-example",
  era: "rome",
  name: "A market street (not drawn yet)",
  walk: { x: [20, 300], y: [150, 194] },
  spawn: { default: [160, 184] },

  hotspots: [
    { id: "stall", name: "fruit stall", rect: [30, 110, 76, 50], walkTo: [70, 176], look: "sketch.stall" },
    { id: "gate", name: "city gate", rect: [128, 52, 64, 66], walkTo: [160, 170], look: "sketch.gate" },
    { id: "cart", name: "cart", verb: "Push", rect: [222, 126, 66, 36], walkTo: [214, 180], look: "sketch.cart", use: "sketch.cart.use" },
  ],
};

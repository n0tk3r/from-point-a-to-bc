// A scene with no picture yet. Leave out `picture` (and `draw`) and the engine sketches
// the place from its clickable areas: sky, ground, and a labelled box for each thing.
// That makes a scene playable as soon as its puzzle is written, so the story can
// be walked through and timed long before any art exists.
//
// The numbers are picture pixels on the 800x600 stage, exactly as they will be when the
// scene is painted: the painter can be handed this file as the layout to paint to.
//
// Try it: index.html?scene=sketch-example&lead=son
// This scene is not part of the story. Delete it when you no longer need the example.

export default {
  id: "sketch-example",
  era: "rome",
  name: "A market street (not painted yet)",
  horizon: 260, full: 590,                    // (the defaults.) The sketch puts its skyline at `horizon`.
  walk: { x: [50, 750], y: [400, 590] },      // a plain box of floor; `area: [[x, y], ...]` gives an outline instead
  spawn: { default: [400, 560] },

  hotspots: [
    { id: "stall", name: "fruit stall", rect: [75, 290, 190, 130], walkTo: [175, 470], look: "sketch.stall" },
    { id: "gate", name: "city gate", rect: [320, 100, 160, 200], walkTo: [400, 430], look: "sketch.gate" },
    { id: "cart", name: "cart", verb: "Push", rect: [555, 330, 165, 95], walkTo: [535, 480], look: "sketch.cart", use: "sketch.cart.use" },
  ],
};

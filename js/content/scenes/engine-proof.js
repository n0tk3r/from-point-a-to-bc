// The worked example of a painted scene: where the wagon came down, by the Nile.
//
// A painted scene is a backdrop picture and a few cut-outs, plus the numbers that let
// people walk about in it. Every number in this file is a pixel on the 800x600 picture,
// so it can be measured straight off the painting.
//
//   picture   the backdrop: everything that is far away or flat on the ground
//   planes    painted cut-outs: PNG files the size of the whole picture with a clear
//             background, laid over it at (0, 0). The engine sorts them with the people.
//   walk      the outline of the ground people can stand on
//   horizon, full   how people shrink as they walk away (see below)
//
// Try it: index.html?scene=engine-proof&lead=dad     (hold H to see an outline round everything that can be clicked)
// This scene is not part of the story. It stays as the pattern to copy, the way
// sketch-example.js is the pattern for a scene that has no painting yet.

const art = "art/scenes/egypt-crash/";
const fx = (g) => !!g.flag("proof.fx");          // the things that move by nature (`fx`, below) are on the stage while this is true

export default {
  id: "engine-proof",
  era: "egypt",
  name: "Where the wagon came down",

  // DEPTH. `horizon` is the row of the picture the ground runs back to, and `full` the row where a person
  // is drawn full size (an adult is 160 pixels tall there). In between, size falls in a straight line:
  //     size = (feet - horizon) / (full - horizon)
  // The painter works from the same two numbers, so doors and wagons come out the right size for the people.
  // minScale stops anyone shrinking to a dot at the far end of the sand.
  horizon: 262, full: 590, minScale: 0.3,

  // WHERE PEOPLE CAN STAND: the sand. The left edge keeps to the bank, clear of the water and of the palms' feet;
  // the far edge stops under the village and the dunes; the right edge keeps a body's width inside the picture.
  walk: { area: [[352, 300], [640, 300], [780, 326], [780, 596], [60, 596], [150, 470], [240, 384], [312, 322]] },
  spawn: { default: [420, 572] },

  picture: art + "back.png",

  // CUT-OUTS. Where each one sorts among the people is its `base`:
  //   a number          the row where it meets the ground. Feet above that row are behind it, feet below in front.
  //   [[x, y], [x, y]]  a line, for a thing that meets the ground on a slant
  //   plane: "front"    in front of everybody, always ("back": behind everybody)
  // `solid` is the patch of ground a cut-out takes up. Nobody can stand in it, and routes go round it.
  planes: [
    // Three palms in a row that runs away from us along the bank: their feet are at (187, 407), (250, 357) and (298, 321),
    // so the base is the line through them. (One row for all three would put people behind a trunk whose foot is behind them.)
    { id: "palms", src: art + "palms.png", base: [[187, 407], [298, 321]] },
    { id: "wagon", src: art + "wagon.png", base: [[490, 541], [790, 537]],        // along the wheels, nose to tail
      solid: [[470, 528], [790, 522], [796, 548], [470, 556]] },                  // the ground under the car (the sand heaped at its nose can be walked behind)
    { id: "papyrus", src: art + "front.png", plane: "front" },                    // the papyrus at the bottom left corner
  ],
  // A cut-out can also follow the story. These are the other forms (none is needed here):
  //   { id: "trunk", src: art + "trunk-open.png", base: 541, when: (g) => g.flag("egypt.trunkOpen") }      a row for a base; shown only while the test passes
  //   { id: "screen", base: 380, state: (g) => (g.flag("home.online") ? "login" : "offline"),              one of several pictures
  //     states: { offline: "art/scenes/home/screen-offline.png", login: "art/scenes/home/screen-login.png" } },
  //   { id: "steam", frames: [art + "steam-0.png", art + "steam-1.png"], fps: 6, at: [520, 470], foot: [20, 60], plane: "front" }
  //                                                         a small cropped picture, animated: its point `foot` is put at `at`
  // `when` and `state` are read again every time the story changes, so a script only records the fact.
  // A script can also take hold of one: g.plane("trunk").show(true), .set("login"), .fade(0.5), .place(x, y, scale).

  // THINGS THAT MOVE BY NATURE (js/engine/effects.js). Nothing that moves by itself in the world is painted still: the
  // painter leaves it out and marks where it goes (layout.json, "fx"), the scene lists it here, and the engine draws it
  // moving, on the game clock, among the people at its own depth (`base` or `plane`, as for a cut-out). They are on the
  // stage only while the story fact "proof.fx" is true (index.html?scene=engine-proof&lead=dad&flags=proof.fx), so that
  // everything else here is as it was. Every kind, every field and its default: docs/DESIGN.md, "Things that move by nature".
  fx: [
    // the builders' village, far off: a cooking fire's smoke, a thin pale thread that rises a little and bends away with the air
    { id: "village-smoke", type: "smoke", at: [392, 286], base: 296, color: "#f4ecdc", opacity: 0.38, height: 36, width: [1.5, 10], lean: [34, -34], when: fx },
    // a fire on the sand: a bed of coals, a flame, and a column of smoke a man can walk behind or in front of (base: where it stands)
    { id: "fire-coals", type: "embers", at: [468, 430], size: [9, 3], base: 430, when: fx },
    { id: "fire", type: "flame", at: [468, 429], size: 13, base: 430, when: fx },
    { id: "fire-smoke", type: "smoke", at: [468, 422], base: 430, height: 130, width: [6, 46], rise: 20, wind: 7, opacity: 0.45, when: fx },
    // light moving on the river, kept off the boat and the reeds; now and then a ring where a fish comes up
    { id: "river", type: "shimmer", when: fx,
      poly: [[0, 264], [344, 264], [321, 276], [295, 300], [261, 336], [213, 384], [149, 440], [83, 492], [19, 530], [0, 532]],
      holes: [[84, 280, 98, 62], [280, 287, 22, 24], [249, 308, 24, 33], [214, 335, 27, 41]] },
    { id: "fish", type: "ripples", at: [206, 300], every: [2, 6], radius: 14, when: fx },
    // doves on the bank between the palms: they peck and potter, go up when somebody comes near, and land again further off
    { id: "doves", type: "birds", look: "dove", count: 6, area: [[268, 372], [318, 334], [372, 338], [392, 372], [330, 402], [282, 400]], when: fx },
    // small birds crossing high up now and then, and two kites wheeling over the pyramid
    { id: "swallows", type: "birds", lanes: [[[-20, 46], [820, 22]], [[820, 62], [-20, 80]]], every: [4, 10], group: [1, 3], when: fx },
    { id: "kites", type: "birds", circle: { at: [560, 58], r: [42, 13] }, count: 2, size: [7, 9], when: fx },
    // the palms' crowns and the papyrus stir in the warm wind off the river (their feet do not move)
    { id: "palms-sway", type: "sway", plane: "palms", anchor: "bottom", amount: 1.4, when: fx },
    { id: "papyrus-sway", type: "sway", plane: "papyrus", anchor: "bottom", amount: 1.2, when: fx },
    // water from a spout, splashing where it lands: here, to show it, meltwater pouring off the roof from the cooler
    { id: "spill", type: "stream", path: [[749, 427], [756, 431], [761, 440], [764, 470], [765, 505], [766, 546]], width: [1.5, 2.5], base: 549, when: fx },
  ],

  // Light that must stay smooth (a wormhole, a beam, a glow) is not painted. A scene draws it live, in the same pixels:
  //   live(art, g) { return art.portal(500, 300, 40, "door"); },        and a script finds it with g.q("#door")

  // WAYS OUT AT THE EDGES OF THE PICTURE. Over the floor near an edge that has one, the pointer becomes an arrow and the
  // label says where it leads ("Go up the track"); a click there walks the lead to that edge, and on (js/engine/edges.js).
  //   N, S, W, E     the top, the bottom, the left and the right of the picture
  //   to, spawn      the scene, and the named way in at the other end, as g.goto(to, { spawn }) takes them
  //   name           what the label says after "Go". With none: "Go to" and the other scene's name.
  //   walkTo         where the lead walks before leaving. With none: the floor nearest the click, as far toward the edge as it goes.
  //   when(g)        the way is there only while this is true (until then its band is plain floor)
  //   use(g)         a script to run instead of the plain g.goto: a way that is also a gate, or that needs a line first
  // A clickable area in a band always wins over it. (This scene has no S edge: the tests click along the front of the sand.)
  edges: {
    N: { to: "sketch-example", name: "up the track", walkTo: [496, 302] },
    E: { to: "sketch-example" },                                                 // the label is "Go to a market street (not painted yet)"
    W: { to: "sketch-example", name: "across the river", when: (g) => !!g.flag("proof.ferry"),
      use: async (g) => { await g.say("egypt.river.look"); await g.goto("sketch-example"); } },
  },

  // CLICKABLE AREAS. Show (or holding H) draws an outline round each, following its poly, rect or circle; so make a shape
  // hug its thing. An area that is a cut-out (`plane: "<plane id>"`, or a plane with the same id, as the wagon here) is
  // outlined by the cut-out's own silhouette instead, as much of it as lies inside the area.
  hotspots: [
    { id: "pyramids", name: "pyramids", rect: [432, 78, 368, 172], look: "egypt.pyramids.look" },
    { id: "river", name: "river", poly: [[0, 262], [345, 262], [20, 530], [0, 545]], walkTo: [200, 440], face: "W", look: "egypt.river.look" },
    { id: "reeds", name: "reeds", poly: [[132, 384], [214, 330], [280, 286], [300, 290], [300, 312], [240, 376], [178, 440], [136, 440]], walkTo: [262, 380], face: "W", look: "egypt.reeds.look" },
    { id: "wagon", name: "wagon", poly: [[462, 492], [560, 470], [600, 420], [650, 388], [750, 394], [790, 440], [790, 520], [740, 544], [462, 520]], walkTo: [600, 574], face: "N", look: "egypt.wagon.look" },
    // The two people (below, under `actors`), while "proof.life" is true: each area is the figure at its mark. Away from
    // the mark on a walk of their own, the area goes with them (js/engine/life.js); a click brings them home to talk.
    { id: "scribe", name: "scribe", verb: "Talk to", rect: [550, 339, 32, 37], walkTo: [604, 384], face: "W", when: (g) => !!g.flag("proof.life"),
      look: "egypt.scribe.look", use: ["egypt.scribe.meet.1"] },
    { id: "overseer", name: "overseer", verb: "Talk to", rect: [279, 364, 44, 114], walkTo: [352, 478], face: "W", when: (g) => !!g.flag("proof.life"),
      look: "egypt.overseer.look", use: ["egypt.overseer.meet.1"] },
  ],

  // PEOPLE, AND THEIR OWN LIVES (js/engine/life.js). Two people of the place, on the stage only while the story fact
  // "proof.life" is true (the engine's test turns it on: index.html?scene=engine-proof&lead=dad&flags=proof.life), so
  // that everything else here is as it was. Everyone fidgets now and then by themselves; `life` says what else they do:
  //   the scribe sits on the sand, and now and then gets up, walks up the bank or over toward the wagon, stays a few
  //   seconds, and comes back and sits down again (a seated person can do this once the rig can stand them up);
  //   the overseer stands, and strolls a few steps toward the river or up the sand, and back.
  // A click on someone who is away brings them home first, while the lead walks over; their clickable area goes with them.
  actors: [
    { id: "scribe", kind: "scribe", at: [566, 372], face: "W", when: (g) => !!g.flag("proof.life"),
      life: { every: [14, 26], spots: [[486, 338, "N"], [660, 356, "E"]], stay: [3, 6] } },
    { id: "overseer", kind: "overseer", at: [300, 470], face: "E", when: (g) => !!g.flag("proof.life"),
      life: { every: [16, 30], spots: [[250, 500, "W"], [380, 420, "N"]], stay: [3, 6] } },
  ],

  // Runs when the lead arrives. It must be safe to run twice (a save can be loaded in the middle of it), so it checks its own fact.
  async enter(g) {
    if (g.flag("proof.arrived")) return;
    await g.wait(400);
    await g.say("egypt.arrive.1");
    g.flag("proof.arrived", true);
  },
};

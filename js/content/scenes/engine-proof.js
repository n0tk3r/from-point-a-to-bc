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
// Try it: index.html?scene=engine-proof&lead=dad     (hold H to see the clickable areas)
// This scene is not part of the story. It stays as the pattern to copy, the way
// sketch-example.js is the pattern for a scene that has no painting yet.

const art = "art/scenes/egypt-crash/";

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

  // Light that must stay smooth (a wormhole, a beam, a glow) is not painted. A scene draws it live, in the same pixels:
  //   live(art, g) { return art.portal(500, 300, 40, "door"); },        and a script finds it with g.q("#door")

  hotspots: [
    { id: "pyramids", name: "pyramids", rect: [432, 78, 368, 172], look: "egypt.pyramids.look" },
    { id: "river", name: "river", poly: [[0, 262], [345, 262], [20, 530], [0, 545]], walkTo: [200, 440], face: "W", look: "egypt.river.look" },
    { id: "reeds", name: "reeds", poly: [[132, 384], [214, 330], [280, 286], [300, 290], [300, 312], [240, 376], [178, 440], [136, 440]], walkTo: [262, 380], face: "W", look: "egypt.reeds.look" },
    { id: "wagon", name: "wagon", poly: [[462, 492], [560, 470], [600, 420], [650, 388], [750, 394], [790, 440], [790, 520], [740, 544], [462, 520]], walkTo: [600, 574], face: "N", look: "egypt.wagon.look" },
  ],

  // Runs when the lead arrives. It must be safe to run twice (a save can be loaded in the middle of it), so it checks its own fact.
  async enter(g) {
    if (g.flag("proof.arrived")) return;
    await g.wait(400);
    await g.say("egypt.arrive.1");
    g.flag("proof.arrived", true);
  },
};

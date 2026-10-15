// MAP-15: the maps. The player opens one with the Map button (or M): the map of the place the lead stands in, with the
// places the player has been to drawn in, their neighbours faint, everyone of the family where they stand, and a way to
// travel back to a place already visited (js/engine/atlas.js draws it; docs/DESIGN.md, "The map, and the Timer").
//
// A map is a sheet of places joined by ways, in one time (`era`, whose notch on the Timer is `eras.<era>.dial` in
// world.js). A place is one scene or several (the wagon's inside is part of "By the river"): the map of a scene is the
// map one of whose places lists it, and a scene that is on no map has no Map button. Travel to a place goes to its first
// scene. A way joins two places, and says for each end the mark of that end's scene where a lead arrives along it (as the
// scenes' own ways out do: their `edges` and the g.goto of their doors and stairs), or a function of the game that says it.
//
//   egypt: {
//     era: "egypt",                                  the time it is in (world.js `eras`)
//     name: "Egypt",                                 the chip's word, at the top of the map screen
//     art: "art/maps/egypt/",                        its painted pictures and their layout.json (the painters'; with none
//                                                    there yet, the engine draws the sketch below)
//     places: {
//       river: { scenes: ["egypt-crash", "egypt-car"], label: "By the river",     its scenes, the first the one travel goes
//                go: "down to the river" },                                       to; the name the engine writes on the map;
//                                                                                 and (seldom) what the label line says after
//                                                                                 "Go", when "Go to" and the name would not
//                                                                                 read well ("Go to the Forum" needs none)
//     },
//     paths: [{ a: "river", b: "site", spawn: { river: "fromSite", site: "fromCrash" } }],    a and b in the painters' order
//     sketch: { places: { river: [180, 470], ... } },                             a pin for each place, laid out as the ways
//   },                                                                            run, for drawing the map with no painting
//
// To add a map: give it an entry here, with every place and way, and a sketch; it is drawn as a sketch until its pictures
// and layout.json are in art/maps/<map>/ (MAP-15.md, "The pictures of a map"). To add a place: its scenes, its label, its
// ways (with the marks their scenes already have), a pin in the sketch, and the painters' picture of it. At every start
// the engine checks this file against the scenes and the eras, and says in the console what does not fit ("Map check").

const cameDown = (g) => (g.flag("egypt.cameDown") ? "fromGalleryAgain" : "fromGallery");     // (as the gallery's way out says: the long stair outside is walked whole only once)

export const maps = {
  // Act One: a papyrus sketch. Up from the river to the foot of the pyramid, in and up the great gallery to the chamber.
  egypt: {
    era: "egypt", name: "Egypt", art: "art/maps/egypt/",
    places: {
      river: { scenes: ["egypt-crash", "egypt-car"], label: "By the river", go: "down to the river" },
      site: { scenes: ["egypt-site"], label: "The foot of the pyramid" },
      gallery: { scenes: ["egypt-gallery"], label: "The great gallery" },
      chamber: { scenes: ["egypt-chamber"], label: "The burial chamber" },
    },
    paths: [
      { a: "river", b: "site", spawn: { river: "fromSite", site: "fromCrash" } },
      { a: "site", b: "gallery", spawn: { site: cameDown, gallery: "fromSite" } },
      { a: "gallery", b: "chamber", spawn: { gallery: "fromChamber", chamber: "fromGallery" } },
    ],
    sketch: { places: { river: [190, 466], site: [320, 338], gallery: [520, 338], chamber: [620, 212] } },
  },

  // Act Two: a wax-tablet plan. Saturn's steps in the middle, the street off to the left, the treasury through the
  // temple's doors, the Forum behind, the Capitol up the hill to the right, and across the Tiber beyond the Forum.
  rome: {
    era: "rome", name: "Rome", art: "art/maps/rome/",
    places: {
      street: { scenes: ["rome-street"], label: "The street" },
      steps: { scenes: ["rome-steps"], label: "Saturn's steps" },
      treasury: { scenes: ["rome-temple"], label: "The treasury" },
      forum: { scenes: ["rome-forum"], label: "The Forum" },
      capitol: { scenes: ["rome-capitol"], label: "The Capitol" },
      tiber: { scenes: ["rome-tiber"], label: "Across the Tiber", go: "across the Tiber" },
    },
    paths: [
      { a: "steps", b: "street", spawn: { steps: "fromStreet", street: "fromForum" } },        // (the street's mark at its far end, so named)
      { a: "steps", b: "treasury", spawn: { steps: "fromTemple", treasury: "default" } },
      { a: "steps", b: "forum", spawn: { steps: "fromForum", forum: "fromSteps" } },
      { a: "steps", b: "capitol", spawn: { steps: "fromCapitol", capitol: "fromSteps" } },
      { a: "forum", b: "tiber", spawn: { forum: "fromTiber", tiber: "fromBridge" } },
    ],
    sketch: { places: { street: [200, 338], steps: [400, 338], treasury: [400, 212], forum: [400, 464], capitol: [600, 338], tiber: [200, 464] } },
  },

  // Act Three: a pencil floor plan of the house. The living room downstairs, the landing at the top of the stairs, and the
  // three rooms off it: Dad's study, Little Sister's room, and up the ladder Big Sister's attic, the Retreat.
  home: {
    era: "home", name: "Home", art: "art/maps/home/",
    places: {
      living: { scenes: ["home-living-room"], label: "The living room" },
      landing: { scenes: ["home-landing"], label: "The landing" },
      study: { scenes: ["home-study"], label: "Dad's study" },
      lilsis: { scenes: ["home-lilsis-room"], label: "Little Sister's room" },
      bigsis: { scenes: ["home-bigsis-room"], label: "The Retreat" },
    },
    paths: [
      { a: "living", b: "landing", spawn: { living: "fromLanding", landing: "fromStairs" } },
      { a: "landing", b: "study", spawn: { landing: "fromStudy", study: "fromLanding" } },
      { a: "landing", b: "lilsis", spawn: { landing: "fromLilsis", lilsis: "fromLanding" } },
      { a: "landing", b: "bigsis", spawn: { landing: "fromLadder", bigsis: "fromLadder" } },
    ],
    sketch: { places: { living: [400, 464], landing: [400, 338], study: [600, 338], lilsis: [200, 338], bigsis: [400, 212] } },
  },

  // Acts Four and Five: a fold-out road map. The Last Stop and Grandpa Joe's store, and on the road, the limousine (which
  // nobody travels to or from: it has no way).
  nevada: {
    era: "nevada", name: "Nevada", art: "art/maps/nevada/",
    places: {
      roadside: { scenes: ["nevada-roadside"], label: "The Last Stop" },
      store: { scenes: ["nevada-store"], label: "Grandpa Joe's store" },
      road: { scenes: ["nevada-limo"], label: "On the road" },
    },
    paths: [
      { a: "roadside", b: "store", spawn: { roadside: "fromStore", store: "fromLot" } },
    ],
    sketch: { places: { roadside: [300, 420], store: [300, 270], road: [580, 340] } },
  },

  // The engine's own proof (js/content/scenes/engine-proof.js, the letterbox): a map for each of its two scenes, drawn as
  // sketches. Dad on the sand in Egypt, the Son in the sketch of a market street in Rome: switching between them is the
  // Timer turning four notches, then the street's map.
  "proof-sand": {
    era: "egypt", name: "Proof sand",
    places: { sand: { scenes: ["engine-proof"], label: "Where the wagon came down" } },
    paths: [],
    sketch: { places: { sand: [400, 350] } },
  },
  "proof-street": {
    era: "rome", name: "Proof street",
    places: { street: { scenes: ["sketch-example"], label: "A market street" } },
    paths: [],
    sketch: { places: { street: [400, 350] } },
  },
};

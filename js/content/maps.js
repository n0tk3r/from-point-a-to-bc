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

  // ENGINE-17: the Office (Act Five, stage one: briefs/out/office-hq-design.md, section 4). A blueprint (PAINT-17B paints it;
  // a sketch until then): the lot outside, the ducts over the ground floor, and the three rooms under them; and B-7, the
  // shaft down, drawn on the sheet always (`shown`) and RESTRICTED: it has no scene yet, and nobody goes there. The only way
  // is the lot to the ducts, by the roof and the unit's intake; the rooms are reached through the grilles in the ducts, not
  // by the map (their grilles are drawn on the blueprint, not as ways). Grandpa Joe and Ranger are in two of its places from
  // the opening on: switching between them is this map, with no Timer (one time). Travel is per lead (`travel` on a place:
  // may he leave it by the map; a line says why not): Grandpa Joe, locked in, goes nowhere ("Locked in, for my comfort.");
  // Ranger, down in a room, climbs back up the way he came (a thought). The line ids are WRITE-17's to write.
  office: {
    era: "nevada", name: "The Office", art: "art/maps/office/",
    places: {
      lot: { scenes: ["office-lot"], label: "The lot" },
      ducts: { scenes: ["office-ducts"], label: "The ducts" },
      // SCENES-17: Ranger's refusal is WRITE-17's line office.map.rooms.ranger ([door, no]: not by a room's door; back up the way he came)
      room: { scenes: ["office-room"], label: "The Comfortable Room", travel: { grandpajoe: "office.map.locked.grandpajoe", ranger: "office.map.rooms.ranger" } },
      property: { scenes: ["office-property"], label: "Property & Effects", travel: { ranger: "office.map.rooms.ranger", any: false } },
      breakroom: { scenes: ["office-breakroom"], label: "The break room", travel: { ranger: "office.map.rooms.ranger", any: false } },
      // SCENES-17: RESTRICTED. A landmark is never travelled to; its `travel` is what a click on it says, whoever is played
      // (js/engine/atlas.js landmarkSays): WRITE-17's map refusals for B-7, Grandpa Joe's words and Ranger's thought.
      b7: { scenes: [], label: "B-7", shown: true, travel: { grandpajoe: "office.map.b7.grandpajoe", ranger: "office.map.b7.ranger" } },
    },
    paths: [
      { a: "lot", b: "ducts", spawn: { lot: "intake", ducts: "intake" } },      // SCENES-17: out of the ducts by the intake, onto the roof in front of the unit
    ],
    // SCENES-17: the sketch's pins where PAINT-17B's blueprint has them (art/maps/office/layout.json), for a page that draws the sketch
    sketch: { places: { lot: [479, 479], ducts: [474, 174], room: [511, 317], property: [369, 269], breakroom: [247, 277], b7: [106, 174] } },
  },

  // ENGINE-20: Act Six, Japan in the spring of 1830 (briefs/out/edo-design.md, section 3): an Edo travel map (PAINT-20B paints
  // it, art/maps/edo/; a sketch until its pictures and layout.json are in), the coast from Suruga Bay in the east to Harima in
  // the west. Its places are PAINT-20B's names (yui, osaka, hills, himeji) and its ways theirs (sea: yui to osaka, over the
  // water; road1: osaka to hills; road2: hills to himeji). The family goes west down it in THREE LEGS (`leg`: Yui; the hills;
  // Himeji): travel by the map only between places of the leg they are in (there is one place to a leg here, so the map is a
  // map and not a vehicle), and a place of a leg behind them shows as visited, drawn in with its name, but refuses with its own
  // line (`far`: WRITE-20A's edo.map.far.yui, "Twelve days by sea."; WRITE-20B's edo.map.far.hills; until they are in, "Too far
  // to go back."). Nobody travels along the ways (`journey: true`: no marks to arrive on): they are the journeys' lines, along
  // which the portraits go in the cut-scenes (g.journey("edo", "yui", "hills", { via: ["osaka"] }) for the voyage and the river
  // mouth; g.journey("edo", "hills", "himeji") for the walk). Osaka is a landmark (no scene: the voyage's card and the river mouth
  // are told, not played). The scenes are ENGINE-20's sketch stubs until SCENES-20's; MERGE-20 joins this entry with PAINT-20B's
  // (theirs has the art and the pins; this one the legs, the far lines and the journeys' ways).
  // PAINT-20B: this entry is ENGINE-20's (S/work-20-engine), copied whole so that MERGE-20 joins the two as a union: theirs has
  // the legs, the far lines and the journeys' ways; the painted map is in art/maps/edo/ (map_edo.py) and its pins are below.
  // ENGINE-21: Act Six made bigger (briefs/out/edo2-design.md, sections 3 and 9): FIVE LEGS. Yui (leg 1: the village, the fish
  // shop, Nishikurasawa and the top of the Satta Pass), Osaka (leg 2: a place now, its three scenes), the hills (leg 3), Akashi
  // (leg 4, new) and Himeji (leg 5: the town, the castle and the keep), with Shosha (leg 5, new: the women's hall, inside it, and
  // its lock), which is not on the map at all until the family knows the way (`known`: edo.knowWay, #36), and then is a place to
  // go to by the map from the town, and back ("An hour and a half's walk, north-west"). Every place behind the family refuses
  // with its own line for the leg they are in (`far`: the line "edo.map.far.<place>.<leg>" if the lines files have it, else
  // "edo.map.far.<place>": WRITE-21B's; "Too far to go back." until either is written).
  // AT SEA: the deck and its compass are a place that is a point of the sea way (`on`, about five days of twelve out: off
  // Daiōzaki): the map shows the family's portraits there on the sea path, and every place refuses with one line (its `travel`:
  // "edo.map.atsea", "We're at sea. The map can wait.": the writers').
  // The journeys' ways are as before; the walk of three days (the hills to Akashi) passes three STOPS, small pictures by the road
  // (Kōriyama, Suma, Maiko: PAINT-21F's), each with a line said over it as the portraits pass (WRITE-21B's edo.walk.stop.*); and
  // the Kyoto boat goes up the river path to Hirakata (a stop with no line: where the river ends and the road begins), then by the
  // road north to the hills. Until PAINT-21F's layout.json has Akashi, Shosha, the new ways and the stops, each is a stand-in on
  // the painting (atlas.js, paintedOf), at the sketch's pins below, near where it belongs; the sea place and the stops on ways
  // are placed on their ways, whatever the painting.
  // The cut-scenes' journeys (phase B's: the calls, docs/DESIGN.md "A journey on the map", ENGINE-21):
  //   Casting Off            g.journey("edo", "yui", "sea", { sound: "creak" })
  //   The Uttermost Parts    g.journey("edo", "sea", "osaka", { sound: "creak" })
  //   The Kyoto Boat         g.journey("edo", "osaka", "hills", { segments: [{ to: "hirakata", sound: "haul" }, { to: "hills", sound: "sandals" }] })
  //   Three days later       g.journey("edo", "hills", "akashi", { sound: "sandals", stops: ["koriyama", "suma", "maiko"], ms: 5200 })
  //   The next day           g.journey("edo", "akashi", "himeji", { sound: "sandals" })
  edo: {
    era: "edo", name: "Japan", art: "art/maps/edo/",
    places: {
      yui: { scenes: ["edo-village", "edo-fishshop", "edo-kurasawa", "edo-satta"], label: "Yui", leg: 1, far: "edo.map.far.yui" },      // (ENGINE-21: and the pass)
      sea: { scenes: ["edo-deck", "edo-compass"], label: "At sea", on: { a: "yui", b: "osaka", at: 0.42 },
        travel: { mom: "edo.map.atsea.mom", bigsis: "edo.map.atsea.bigsis", lilsis: "edo.map.atsea.lilsis" } },      // ENGINE-21: at sea (SCENES-21A: WRITE-21A's line for each of the three; was "edo.map.atsea", not written)
      osaka: { scenes: ["edo-dojima", "edo-street", "edo-theatre"], label: "Osaka", leg: 2, far: "edo.map.far.osaka" },      // (ENGINE-21: a place now, not a landmark)
      hills: { scenes: ["edo-cedars", "edo-storehouse", "edo-chapel"], label: "The hills", leg: 3, far: "edo.map.far.hills" },
      akashi: { scenes: ["edo-akashi"], label: "Akashi", leg: 4, far: "edo.map.far.akashi" },      // ENGINE-21
      himeji: { scenes: ["edo-town", "edo-castle", "edo-keep", "edo-keeptop"], label: "Himeji", leg: 5, far: "edo.map.far.himeji" },      // (ENGINE-21: the town first)
      shosha: { scenes: ["edo-shosha", "edo-hall", "edo-lock"], label: "Shosha", leg: (g) => (g.flag("edo.nightDone") ? 0 : 5), far: "edo.map.shosha.done", known: (g) => !!g.flag("edo.knowWay"), go: "to the women's hall at Shosha" },      // ENGINE-21 (SCENES-21C: the next day, Shosha is behind them: "Shosha's done its part. Today it's the castle.")
    },
    paths: [
      { a: "yui", b: "osaka", journey: true },        // the sea: the voyage (twelve days)
      { a: "osaka", b: "hills", journey: true },      // the river path up the Yodo, then the road north into the hills (ENGINE-21: the Kyoto boat)
      { a: "hills", b: "akashi", journey: true },     // ENGINE-21: the road west, three days (Kōriyama, Suma, Maiko)
      { a: "akashi", b: "himeji", journey: true },    // ENGINE-21: the road on to Himeji, a day
      { a: "himeji", b: "shosha", spawn: { himeji: "gate", shosha: "road" } },      // ENGINE-21: an hour and a half's walk, north-west (travelled)
    ],
    // ENGINE-21: the stops, small pictures by the way: each `on` a way (or with a pin of the painters'), its `line` said as a
    // journey's portraits come to it, `shown` once the family has gone by (so the map keeps them after)
    stops: {
      hirakata: { label: "Hirakata", on: { a: "osaka", b: "hills", near: [344, 356] } },
      koriyama: { label: "Kōriyama", on: { a: "hills", b: "akashi", at: 0.14 }, line: "edo.walk.stop.koriyama", shown: (g) => !!g.flag("edo.walked") },
      suma: { label: "Suma", on: { a: "hills", b: "akashi", at: 0.52 }, line: "edo.walk.stop.suma", shown: (g) => !!g.flag("edo.walked") },
      maiko: { label: "Maiko", on: { a: "hills", b: "akashi", at: 0.78 }, line: "edo.walk.stop.maiko", shown: (g) => !!g.flag("edo.walked") },
    },
    // PAINT-20B: the sketch's pins where the painted map has them (art/maps/edo/layout.json), for a page that draws the sketch
    // (ENGINE-21: and the new places' stand-ins near where they belong: Akashi on the coast road east of Himeji, Shosha north-west of it)
    sketch: { places: { yui: [640, 312], osaka: [300, 448], hills: [300, 308], akashi: [205, 368], himeji: [130, 296], shosha: [100, 262] } },
  },

  // The engine's own proof (js/content/scenes/engine-proof.js, the letterbox): a map for each of its two scenes, drawn as
  // sketches. Dad on the sand in Egypt, the Son in the sketch of a market street in Rome: switching between them is the
  // Timer turning four notches, then the street's map.
  // ENGINE-17: and under the sand, a room of the same time (proof-below.js), joined to the sand by a way: two leads in two
  // scenes of one time switch through this map with no Timer; its travel is per lead (Dad may not leave it by the map: the
  // place says so here; the critter may not: the scene says so).
  // ENGINE-20: and the legs, proved here: while the fact "proof.legs" is true the sand is leg 1 and the room under it leg 2, so
  // that from either the other is "far" (the sand's far is a line of the proof's, the room's a thought); without the fact,
  // neither has a leg and the map is as it was. The way between them is kept for travel; a second way, `journey` only, runs
  // round by the dunes (the proof's journey goes along it: proof.journey in engine-proof.js).
  // ENGINE-21: and round twenty-one's: the close-up of the strongbox is part of the sand (proof-near); a boat on the river is a
  // place that is a point of the way round by the dunes (`on`: at sea, as Act Six's deck is: its travel says why not); the way
  // round by the dunes has two stops, each with a line (the journeys' pictures by the way: proof.stops)
  "proof-sand": {
    era: "egypt", name: "Proof sand",
    places: { sand: { scenes: ["engine-proof", "proof-near"], label: "Where the wagon came down", leg: (g) => (g.flag("proof.legs") ? 1 : null), far: "proof.far.sand" },      // (ENGINE-21: and its close-up)
      boat: { scenes: ["proof-boat"], label: "On the river", on: { a: "sand", b: "dunes", at: 0.5 }, travel: "proof.atsea" },      // ENGINE-21: at sea
      below: { scenes: ["proof-below"], label: "Under the sand", travel: { dad: "proof.travel.dad" }, leg: (g) => (g.flag("proof.legs") ? 2 : null), far: "proof.far.below" },      // ENGINE-17 (ENGINE-20: the legs)
      dunes: { scenes: [], label: "The dunes", shown: (g) => !!g.flag("proof.journey"), leg: (g) => (g.flag("proof.legs") ? 2 : null) } },      // ENGINE-20: a landmark the journey passes
    paths: [{ a: "sand", b: "below", spawn: { sand: "grate", below: "fromSand" } },                           // ENGINE-17
      { a: "sand", b: "dunes", journey: true }, { a: "dunes", b: "below", journey: true }],                   // ENGINE-20: the journey's way, round by the dunes
    stops: { well: { label: "A well", on: { a: "sand", b: "dunes", at: 0.25 }, line: "proof.stop.well" },          // ENGINE-21: a journey's stops
      oasis: { label: "An oasis", on: { a: "dunes", b: "below", at: 0.5 }, line: "proof.stop.oasis", shown: (g) => !!g.flag("proof.stopped") } },
    sketch: { places: { sand: [400, 280], below: [400, 440], dunes: [620, 360] } },
  },
  "proof-street": {
    era: "rome", name: "Proof street",
    places: { street: { scenes: ["sketch-example"], label: "A market street" } },
    paths: [],
    sketch: { places: { street: [400, 350] } },
  },
};

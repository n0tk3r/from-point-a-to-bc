// The list of scenes. A scene is one file in this folder, named after its id.
// To add a scene: write the file, then add its id here.
// The engine fetches all of them while the start-up panel is showing, so that a game in
// progress never has to ask the server for code (and so can never be handed a newer
// version's scene in the middle of an older version's game). They are a few KB each.
// When there are hundreds, fetch them an act at a time instead.
// (A scene's pictures are another matter: once the title is up they are all fetched quietly in the background.)

export const sceneIds = [
  "egypt-crash", "egypt-car", "egypt-site", "egypt-gallery", "egypt-chamber",     // Act One (CAR-13S: egypt-car, the inside of the wagon)
  "rome-steps", "rome-street", "rome-temple", "rome-forum", "rome-capitol", "rome-tiber",   // Act Two (ROME-13S: the Forum, the Capitol, across the Tiber)
  "home-living-room", "home-landing", "home-study", "home-lilsis-room", "home-bigsis-room",   // Act Three
  "nevada-roadside", "nevada-store",                                 // Act Four (NEVADA-12SB: the store)
  "nevada-limo",                                                     // Act Five (NEVADA-12SC)
  "office-lot", "office-ducts", "office-room", "office-property", "office-breakroom",     // Act Five, continued: the Office (SCENES-17; office-common.js, beside them, is what they share: not a scene)
  // ENGINE-20: Act Six, Japan in 1830 (briefs/out/edo-design.md). The eight are the engine's sketch stubs until SCENES-20 writes
  // them (each file says so): the village first, where Going Down hands the game on (cutscenes/office-down.js, edo-arrive.js).
  "edo-village", "edo-fishshop", "edo-cedars", "edo-storehouse", "edo-chapel", "edo-castle", "edo-keep", "edo-keeptop",
  // ENGINE-21: Act Six made bigger (briefs/out/edo2-design.md): the twelve new scenes, the engine's sketch stubs until phase B's
  // SCENES-21A, 21B and 21C write them (each file says so): the pass, the deck and its close-up, Osaka's three, Akashi, Himeji's
  // town, the women's hall at Shosha, inside it, and its lock (a close-up)
  "edo-kurasawa", "edo-satta", "edo-deck", "edo-compass", "edo-dojima", "edo-street", "edo-theatre", "edo-akashi", "edo-town",
  "edo-shosha", "edo-hall", "edo-lock",
  "engine-proof",        // not part of the story: the worked example of a painted scene
  "sketch-example",      // not part of the story: shows how to storyboard a scene before it is painted
  "proof-below",         // not part of the story: ENGINE-17's room under the proof's sand, for the grille, a thing handed across, travel per lead
  "proof-boat",          // not part of the story: ENGINE-21's boat on the river (at sea on the map; the ship's moving things)
  "proof-near",          // not part of the story: ENGINE-21's close-up (a strongbox seen close: hands, the moment's facts, Step back)
];

export const loadScene = (id) => import(`./${id}.js`).then((module) => module.default);

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
  "engine-proof",        // not part of the story: the worked example of a painted scene
  "sketch-example",      // not part of the story: shows how to storyboard a scene before it is painted
  "proof-below",         // not part of the story: ENGINE-17's room under the proof's sand, for the grille, a thing handed across, travel per lead
];

export const loadScene = (id) => import(`./${id}.js`).then((module) => module.default);

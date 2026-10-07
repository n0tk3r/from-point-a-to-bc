// The list of scenes. A scene is one file in this folder, named after its id.
// To add a scene: write the file, then add its id here.
// The engine fetches all of them while the start-up panel is showing, so that a game in
// progress never has to ask the server for code (and so can never be handed a newer
// version's scene in the middle of an older version's game). They are a few KB each.
// When there are hundreds, fetch them an act at a time instead.
// (A scene's pictures are another matter: once the title is up they are all fetched quietly in the background.)

export const sceneIds = [
  "egypt-crash", "egypt-site", "egypt-gallery", "egypt-chamber",     // Act One
  "rome-steps", "rome-street", "rome-temple",                        // Act Two
  "home-living-room",                                                // Act Three
  "nevada-roadside",                                                 // Act Four
  "engine-proof",        // not part of the story: the worked example of a painted scene
  "sketch-example",      // not part of the story: shows how to storyboard a scene before it is painted
];

export const loadScene = (id) => import(`./${id}.js`).then((module) => module.default);

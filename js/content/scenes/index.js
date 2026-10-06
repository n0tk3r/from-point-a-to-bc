// The list of scenes. A scene is one file in this folder, named after its id.
// To add a scene: write the file, then add its id here.
// Scene files are fetched only when the player gets there, so the game starts
// just as fast with two hundred scenes as with two.

export const sceneIds = [
  "egypt-riverbank",
  "rome-forum",
  "sketch-example",      // not part of the story: shows how to storyboard a scene before it is drawn
];

export const loadScene = (id) => import(`./${id}.js`).then((module) => module.default);

// NEVADA-12E: the painted figures: the people of the game who are not drawn by the rig but painted, frame by frame,
// like the donkey and the birds, and yet walk, talk, are clicked on, carry things and can be played: an animal. Each
// one is a sidecar file beside its frames (docs/DESIGN.md, section 4, "Painted frame by frame"), and this is the list of
// them: a kind, as `sprite` names it in js/content/world.js and `kind` in a scene's `actors`, and where its sidecar is.
// Whoever makes figures (cast.js, addFigure) makes a painted one for a kind that is listed here, and a rig one for any
// other. The sidecars and the portraits are fetched when the game starts, with the scene files, so that a portrait is
// here the moment the team bar first wants it; the frames come with the pictures of the scene they stand in.

export const painted = {
  ranger: "art/scenes/nevada-roadside/ranger.json",      // Grandpa Joe's raccoon (PAINT-12C paints him)
  critter: "art/proof/critter.json",                     // the engine's own creature, for the proof scene (painted by a script, critter.py, kept beside the game with the engine's test)
};

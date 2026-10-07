// Every spoken line in the game, in English.
//   "line.id": ["who", "What they say."]
// Scripts refer to lines by ID only. A voice recording for a line is a sound file
// named after its ID (see js/content/sound.js). A translation is a copy of the
// files in js/content/lines/ with the same IDs.
//
// The lines are kept one file to an act, so that an act can be written, read aloud
// and recorded as a piece. This file only gathers them.
// docs/CHARACTERS.md says how each of the family talks. Two rules from it:
//   a line belongs to one person (if anybody could have said it, rewrite it), and
//   every fact Big Sister states is true (docs/CHARACTERS.md lists them, and which have been checked).

import { lines as common } from "./lines/common.en.js";
import { lines as egypt } from "./lines/egypt.en.js";
import { lines as rome } from "./lines/rome.en.js";
import { lines as home } from "./lines/home.en.js";
import { lines as nevada } from "./lines/nevada.en.js";

export const lines = {};
for (const [act, part] of Object.entries({ common, egypt, rome, home, nevada })) {
  for (const [id, line] of Object.entries(part)) {
    if (lines[id]) console.warn(`Line "${id}" is written twice (the second time in lines/${act}.en.js).`);
    lines[id] = line;
  }
}

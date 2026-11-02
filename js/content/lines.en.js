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
import { lines as limo } from "./lines/limo.en.js";                  // NEVADA-12W: Act Five opens, in the limousine
import { lines as office } from "./lines/office.en.js";              // WRITE-17: Act Five continued, the Office (stage one)
import { lines as edoA } from "./lines/edo-a.en.js";                 // WRITE-20A: Act Six, Japan 1830: the arrival, Yui (#21-#24), the voyage, the act's common lines
import { lines as edoB } from "./lines/edo-b.en.js";                 // WRITE-20B: Act Six, the second and third legs (#25-#30, the step)
import { lines as edoC } from "./lines/edo-c.en.js";                 // WRITE-21A: Act Six made bigger, column A: the pass, the ship, Osaka, the Kyoto boat
import { lines as edoD } from "./lines/edo-d.en.js";                 // WRITE-21B: Act Six made bigger: the walk, Akashi, Himeji town, Shosha, the Son (#35-#38)

export const lines = {};
for (const [act, part] of Object.entries({ common, egypt, rome, home, nevada, limo, office, "edo-a": edoA, "edo-b": edoB, "edo-c": edoC, "edo-d": edoD })) {      // NEVADA-12W: limo; WRITE-17: office; WRITE-20A/B: Act Six in two halves  // WRITE-21A/B: C and D (round twenty-one)
  for (const [id, line] of Object.entries(part)) {
    if (lines[id]) console.warn(`Line "${id}" is written twice (the second time in lines/${act}.en.js).`);
    lines[id] = line;
  }
}

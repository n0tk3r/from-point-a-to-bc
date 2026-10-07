// The story, as a list of acts and beats. This file is the game's storyboard.
// Open tools/storyboard.html in a browser to see it laid out, with every scene drawn.
//
// A beat is one step of the story:
//   id      a short name
//   kind    "cutscene", "puzzle" or "gate" (the puzzle that ends the act)
//   chain   puzzles with the same letter follow one another; different letters can be
//           done in any order. Two or three chains per act keeps the player from
//           getting stuck on one thing.
//   lead    who does it: a lead's id ("dad", "lilsis"), a list of ids, or a group from `groups` below
//   scene   where it happens
//   needs   facts that must be true first
//   sets    the fact this beat makes true (scripts call g.flag(sets, true))
//   hint    the line the lead says when the player asks for help. In a team it is one line for
//           each lead: the one who does the job says what to try, the others say whose job it is.
//
// Each act is its own file in js/content/acts/, and has a puzzle document in docs/.

import { act as prologue } from "./acts/prologue.js";
import { act as egypt } from "./acts/egypt.js";
import { act as rome } from "./acts/rome.js";
import { act as home } from "./acts/home.js";
import { act as nevada } from "./acts/nevada.js";

export const story = {
  // Where a new game begins, and the facts that are already true by then
  // (the intro movie has played before the first scene).
  start: { scene: "egypt-crash", lead: "dad", flags: ["seen.intro"] },

  // Names for more than one lead at once.
  groups: { both: ["dad", "son"], family: ["mom", "bigsis", "lilsis"] },

  // Stock replies, one list for each lead.
  fallbacks: {
    nope: {
      dad: ["nope.dad.1", "nope.dad.2", "nope.dad.3"], son: ["nope.son.1", "nope.son.2", "nope.son.3"],
      mom: ["nope.mom.1", "nope.mom.2", "nope.mom.3"], bigsis: ["nope.bigsis.1", "nope.bigsis.2", "nope.bigsis.3"], lilsis: ["nope.lilsis.1", "nope.lilsis.2", "nope.lilsis.3"],
    },
    look: { dad: ["look.dad.1"], son: ["look.son.1"], mom: ["look.mom.1"], bigsis: ["look.bigsis.1"], lilsis: ["look.lilsis.1"] },
    hint: { dad: ["hint.dad.none"], son: ["hint.son.none"], mom: ["hint.mom.none"], bigsis: ["hint.bigsis.none"], lilsis: ["hint.lilsis.none"] },
  },

  // What a lead says on looking at a companion, and on handing one of them something.
  see: {
    mom: { bigsis: "see.mom.bigsis", lilsis: "see.mom.lilsis" },
    bigsis: { mom: "see.bigsis.mom", lilsis: "see.bigsis.lilsis" },
    lilsis: { mom: "see.lilsis.mom", bigsis: "see.lilsis.bigsis" },
  },
  give: { dad: ["give.dad.1"], son: ["give.son.1"], mom: ["give.mom.1"], bigsis: ["give.bigsis.1"], lilsis: ["give.lilsis.1"] },

  // The acts, in order. Each is its own file in js/content/acts/.
  acts: [prologue, egypt, rome, home, nevada],
};

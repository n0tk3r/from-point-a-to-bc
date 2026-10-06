// The story, as a list of acts and beats. This file is the game's storyboard.
// Open tools/storyboard.html in a browser to see it laid out, with every scene drawn.
//
// A beat is one step of the story:
//   id      a short name
//   kind    "cutscene", "puzzle" or "gate" (the puzzle that ends the act)
//   chain   puzzles with the same letter follow one another; different letters can be
//           done in any order. Two or three chains per act keeps the player from
//           getting stuck on one thing.
//   lead    who does it: "dad", "son" or "both"
//   scene   where it happens
//   needs   facts that must be true first
//   sets    the fact this beat makes true (scripts call g.flag(sets, true))
//   hint    the line the lead says when the player asks for help
//
// PLACEHOLDER CONTENT: a tiny story that exercises every part of the engine.
// Replace it act by act as the real puzzle document is written.

export const story = {
  // Where a new game begins, and the facts that are already true by then
  // (the intro movie has played before the first scene).
  start: { scene: "egypt-riverbank", lead: "dad", flags: ["seen.intro"] },

  fallbacks: {
    nope: { dad: ["nope.dad.1", "nope.dad.2", "nope.dad.3"], son: ["nope.son.1", "nope.son.2"] },
    look: { dad: ["look.dad.1"], son: ["look.son.1"] },
    hint: { dad: ["hint.dad.none"], son: ["hint.son.none"] },
  },

  acts: [
    {
      id: 0, title: "Prologue: The Shortcut", era: "present", gate: "seen.intro",
      summary: "Dad takes a shortcut. The sky opens, the road sign changes its mind, and the wagon drives into a hole in time. Father and son are pulled apart in the tunnel.",
      beats: [
        { id: "intro", kind: "cutscene", title: "The shortcut", lead: "both", scene: "intro", needs: [], sets: "seen.intro" },
      ],
    },
    {
      id: 1, title: "Act One: Scattered", era: "egypt", gate: "egypt.ready",
      summary: "Dad lands by the Nile, alone. A scribe saw the boy leave through a door in the air. To follow, Dad has to get the door to hold still.",
      beats: [
        { id: "egypt.arrive", kind: "cutscene", title: "Crash landing by the Nile", lead: "dad", scene: "egypt-riverbank", needs: ["seen.intro"], sets: "egypt.arrived" },
        { id: "egypt.reed", kind: "puzzle", chain: "A", title: "Cut a reed by the river", lead: "dad", scene: "egypt-riverbank", needs: ["egypt.arrived"], sets: "egypt.hasReed", hint: "hint.egypt.reed" },
        { id: "egypt.pen", kind: "puzzle", chain: "A", title: "Give the scribe a new pen", lead: "dad", scene: "egypt-riverbank", needs: ["egypt.hasReed"], sets: "egypt.penGiven", hint: "hint.egypt.pen" },
        { id: "egypt.map", kind: "puzzle", chain: "B", title: "Find the road map in the wagon", lead: "dad", scene: "egypt-riverbank", needs: ["egypt.arrived"], sets: "egypt.hasMap", hint: "hint.egypt.map" },
        { id: "egypt.mark", kind: "puzzle", chain: "B", title: "Have the scribe mark the door's path on the map", lead: "dad", scene: "egypt-riverbank", needs: ["egypt.hasMap", "egypt.penGiven"], sets: "egypt.mapMarked", hint: "hint.egypt.mark" },
        { id: "egypt.leave", kind: "gate", title: "Step up to the humming door", lead: "dad", scene: "egypt-riverbank", needs: ["egypt.mapMarked"], sets: "egypt.ready", hint: "hint.egypt.leave" },
      ],
    },
    {
      id: 2, title: "Act Two: Meanwhile", era: "rome", gate: "demo.done",
      summary: "The Son has landed in Rome. From here the player can switch between the two of them, and things sent through a door in one era turn up in another.",
      beats: [
        { id: "rome.arrive", kind: "cutscene", title: "Not the rest stop", lead: "son", scene: "rome-forum", needs: ["egypt.ready"], sets: "rome.arrived" },
        { id: "rome.coin", kind: "puzzle", chain: "A", title: "Borrow a wish from the fountain", lead: "son", scene: "rome-forum", needs: ["rome.arrived"], sets: "rome.hasCoin", hint: "hint.rome.coin" },
        { id: "rome.toss", kind: "gate", title: "Toss the coin through the door", lead: "son", scene: "rome-forum", needs: ["rome.hasCoin"], sets: "demo.done", hint: "hint.rome.toss" },
      ],
    },
  ],
};

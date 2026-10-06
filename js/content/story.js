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
// PLACEHOLDER CONTENT: a small story that exercises every part of the engine.
// Replace it act by act as the real puzzle document is written.

const family = (id) => ({ mom: `hint.${id}.mom`, bigsis: `hint.${id}.bigsis`, lilsis: `hint.${id}.lilsis` });

export const story = {
  // Where a new game begins, and the facts that are already true by then
  // (the intro movie has played before the first scene).
  start: { scene: "egypt-riverbank", lead: "dad", flags: ["seen.intro"] },

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
      id: 2, title: "Act Two: Meanwhile", era: "rome", gate: "rome.tossed",
      summary: "The Son has landed in Rome. From here the player can switch between the two of them, and things sent through a door in one era turn up in another.",
      beats: [
        { id: "rome.arrive", kind: "cutscene", title: "Not the rest stop", lead: "son", scene: "rome-forum", needs: ["egypt.ready"], sets: "rome.arrived" },
        { id: "rome.coin", kind: "puzzle", chain: "A", title: "Borrow a wish from the fountain", lead: "son", scene: "rome-forum", needs: ["rome.arrived"], sets: "rome.hasCoin", hint: "hint.rome.coin" },
        { id: "rome.toss", kind: "gate", title: "Toss the coin through the door", lead: "son", scene: "rome-forum", needs: ["rome.hasCoin"], sets: "rome.tossed", hint: "hint.rome.toss" },
      ],
    },
    {
      id: 3, title: "Act Three: Five Places Set", era: "home", gate: "home.left",
      summary: "The present, that evening. Dinner is cold and two chairs are empty. Mom and the girls set out to learn where Dad's phone was last seen: Little Sister gets the router going from inside the closet under the stairs, Big Sister works out the password from a date she happens to know, and Mom answers the one question only she can.",
      beats: [
        { id: "home.arrive", kind: "cutscene", title: "Voicemail, for the ninth time", lead: "family", scene: "home-living-room", needs: ["rome.tossed"], sets: "home.arrived" },
        { id: "home.router", kind: "puzzle", chain: "A", title: "Plug the router back in, from inside the closet", lead: "lilsis", scene: "home-living-room", needs: ["home.arrived"], sets: "home.online", hint: family("home.router") },
        { id: "home.note", kind: "puzzle", chain: "B", title: "Work out the password from Dad's note", lead: "bigsis", scene: "home-living-room", needs: ["home.arrived"], sets: "home.knowsYear", hint: family("home.note") },
        { id: "home.login", kind: "puzzle", chain: "C", title: "Sign in, and answer the question about the wedding", lead: "mom", scene: "home-living-room", needs: ["home.online", "home.knowsYear"], sets: "home.foundPing", hint: family("home.login") },
        { id: "home.leave", kind: "gate", title: "Out of the front door, to Nevada", lead: "family", scene: "home-living-room", needs: ["home.foundPing"], sets: "home.left", hint: family("home.leave") },
      ],
    },
    {
      id: 4, title: "Act Four: The Last Stop Before Nothing", era: "nevada", gate: "demo.done",
      summary: "The middle of Nevada, the next morning. A witness saw the wagon drive into the sky, and the government has fenced off the desert for 'elevated radiation'. Mom gets the witness talking, Little Sister keeps the man in gray busy, and Big Sister reads a coin and a notice and sees that the closed sectors are not places but years.",
      beats: [
        { id: "nevada.arrive", kind: "cutscene", title: "Where the map stops", lead: "family", scene: "nevada-roadside", needs: ["home.left"], sets: "nevada.arrived" },
        { id: "nevada.witness", kind: "puzzle", chain: "A", title: "Ask the old-timer nicely, and prove you are family", lead: "mom", scene: "nevada-roadside", needs: ["nevada.arrived"], sets: "nevada.witness", hint: family("nevada.witness") },
        { id: "nevada.coin", kind: "puzzle", chain: "A", title: "Hand Big Sister the coin that fell out of the sky", lead: "bigsis", scene: "nevada-roadside", needs: ["nevada.witness"], sets: "nevada.coinRead", hint: family("nevada.coin") },
        { id: "nevada.distract", kind: "puzzle", chain: "B", title: "Ask the man in gray two hundred questions", lead: "lilsis", scene: "nevada-roadside", needs: ["nevada.arrived"], sets: "nevada.distracted", hint: family("nevada.distract") },
        { id: "nevada.notice", kind: "puzzle", chain: "B", title: "Read the notice on the fence", lead: "bigsis", scene: "nevada-roadside", needs: ["nevada.distracted"], sets: "nevada.notice", hint: family("nevada.notice") },
        { id: "nevada.tracks", kind: "gate", title: "Stand where the tire tracks stop", lead: "family", scene: "nevada-roadside", needs: ["nevada.coinRead", "nevada.notice"], sets: "demo.done", hint: family("nevada.tracks") },
      ],
    },
  ],
};

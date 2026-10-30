// Act Six's shared pieces (MERGE-20: new in round twenty), for the eight scenes of Japan, spring 1830. What is here is
// used by more than one leg; a leg's own helpers stay in its own scene files. SCENES-20A, 20B and 20C: add nothing here
// (say in ready.md what you would have added, and MERGE-20 will).
//
//   is, has            a fact; a thing in someone's pockets
//   STOCK              the act's own stock replies (the scene field `stock`, SCENES-17's): Mom's, Big Sister's and Little
//                      Sister's "no", "nothing there", "no hint" and "give" lines for Japan (WRITE-20A's, lines/edo-a.en.js)
//   SEE                what each of the three says on looking at another, once they are in O-Tami's clothes (edo.clothes);
//                      before that, the story's own `see` lines (their Nevada ones) are right
//   stockFor(g)        STOCK with SEE once edo.clothes is true: a scene's `stock` getter can return it (see below)
//   LEG_START          for the tests: where each leg begins (the act's three legs), and what is true and carried there
//
// The engine reads `scene.stock` from the scene object (game.js stockOf). The two scenes of Yui, where the clothes change,
// set it in `enter` and again after O-Tami's dress hook: `this.stock = stockFor(g)`. From the cedar path on the clothes
// are always on, so those scenes simply have `stock: STOCK_DRESSED`.

export const is = (g, fact) => !!g.flag(fact);
export const has = (g, who, item) => ((g.store.data.inventory || {})[who] || []).includes(item);

export const STOCK = {
  nope: { mom: ["edo.nope.mom.1", "edo.nope.mom.2", "edo.nope.mom.3"], bigsis: ["edo.nope.bigsis.1", "edo.nope.bigsis.2", "edo.nope.bigsis.3"],
    lilsis: ["edo.nope.lilsis.1", "edo.nope.lilsis.2", "edo.nope.lilsis.3"] },
  look: { mom: ["edo.look.mom.1"], bigsis: ["edo.look.bigsis.1"], lilsis: ["edo.look.lilsis.1"] },
  hint: { mom: ["edo.hint.none.mom"], bigsis: ["edo.hint.none.bigsis"], lilsis: ["edo.hint.none.lilsis"] },
  give: { mom: ["edo.give.mom.1"], bigsis: ["edo.give.bigsis.1"], lilsis: ["edo.give.lilsis.1"] },
};

export const SEE = {
  mom: { bigsis: "edo.see.mom.bigsis", lilsis: "edo.see.mom.lilsis" },
  bigsis: { mom: "edo.see.bigsis.mom", lilsis: "edo.see.bigsis.lilsis" },
  lilsis: { mom: "edo.see.lilsis.mom", bigsis: "edo.see.lilsis.bigsis" },
};

export const STOCK_DRESSED = { ...STOCK, see: SEE };
export const stockFor = (g) => (is(g, "edo.clothes") ? STOCK_DRESSED : STOCK);

/** Where each leg begins, for a play or a check that starts a leg on its own (MERGE-20's integration play runs the
    three in a row from the Office's end instead). `outfit` is PEOPLE-20's (g.dress); `pockets` what each carries. */
export const LEG_START = {
  yui: { scene: "edo-village", spawn: "arrive", flags: ["office.done"], outfit: null,
    pockets: { bigsis: ["coin"], lilsis: ["egg", "lilflash"] } },
  hills: { scene: "edo-cedars", spawn: "enter", outfit: "edo",
    flags: ["office.done", "edo.arrived", "edo.clue.red", "edo.clue.coins", "edo.clue.blue", "edo.when", "edo.clerkPassed",
      "edo.babySleeps", "edo.clothes", "edo.dressed", "edo.kiheiMet", "edo.fed", "edo.boxGiven", "edo.hensWest", "edo.kiheiWest",
      "edo.gonrokuNo", "edo.gonrokuWife", "edo.west", "edo.sailed", "edo.arigato"],
    pockets: { bigsis: ["coin"], lilsis: ["egg", "lilflash"] } },
  himeji: { scene: "edo-castle", spawn: "enter", outfit: "edo",
    flags: ["office.done", "edo.arrived", "edo.when", "edo.clothes", "edo.dressed", "edo.fed", "edo.west", "edo.sailed", "edo.arigato",
      "edo.pipeHeard", "edo.unbarred", "edo.hidden", "edo.roomMet", "edo.prayed", "edo.altarOpen", "edo.verse", "edo.laughed",
      "edo.trusted", "edo.watch", "edo.sacksHid", "edo.pinkOff", "edo.momBelow", "edo.eggGiven", "edo.constableGone", "edo.mirror",
      "edo.walked"],
    pockets: { mom: ["mirror", "trowel"], bigsis: ["coin"], lilsis: ["lilflash"] } },
};

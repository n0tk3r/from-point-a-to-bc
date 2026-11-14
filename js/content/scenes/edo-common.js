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
    three in a row from the Office's end instead). `outfit` is PEOPLE-20's (g.dress); `pockets` what each carries.
    ENGINE-21: Act Six made bigger (briefs/out/edo2-design.md, section 7): seven starts now, each with the facts of every beat
    before it (the beats' and their stages': section 7's table and each puzzle card's; round twenty's as its checkpoints were
    played) and the pockets of section 7's "things the family carries" table. `tunnel` (the castle's): what waits in the tunnel
    (the rice ball, through the small door at Shosha, for the Son). The scenes may adjust them in phase B. */
// ENGINE-21: the facts as the act goes, leg by leg (each list the facts its leg adds)
const YUI = ["office.done", "edo.arrived", "edo.arigato", "edo.babySleeps", "edo.boardRead", "edo.boxGiven", "edo.bunsei", "edo.catGone",
  "edo.clerkPassed", "edo.clothes", "edo.clue.blue", "edo.clue.coins", "edo.clue.red", "edo.dressed", "edo.fed", "edo.gonrokuMet",
  "edo.gonrokuNo", "edo.gonrokuWife", "edo.hensWest", "edo.kiheiMet", "edo.kiheiWest", "edo.masaAsked", "edo.masaMet", "edo.pennyShown",
  "edo.saidArigato", "edo.sankichiMet", "edo.tamiMet", "edo.west", "edo.when",
  // SCENES-21A: #24, the road over the pass, as play-edo-yui.py plays it before Casting Off (Kihei's road first; O-Kuni, the
  // bearers, Sōshichi; the top: the gust, the pass found and given back, Arai, the cloud lifted, the old shore; Mosuke back
  // with a new load; O-Shige gone on east; O-Kuni's "Back down.")
  "edo.kiheiRoad", "edo.kuniMet", "edo.shellShared", "edo.araiWarned", "edo.bearersMet", "edo.soshichiMet", "edo.printGiven",
  "edo.gust", "edo.mosukeMet", "edo.shigeMet", "edo.passFound", "edo.passBack", "edo.araiHeard", "edo.fujiClear", "edo.oldShoreHeard", "edo.noRoad",
  "edo.mosukeBack", "edo.shigeGone", "edo.kuniBack"];                                                       // (#24, West: the road; round twenty-one)
const CASTOFF = ["edo.aboard"];                                                                             // Casting Off
const DECK = ["edo.kanbeiMet", "edo.boxSeen", "edo.cardShaded", "edo.compassRead", "edo.englishTried", "edo.saruSaid", "edo.seaWords", "edo.headingCalled",      // #26 Etekō (SCENES-21A: as play-edo-deck.py plays it)
  "edo.kotaMet", "edo.saruHeard", "edo.denzoMet", "edo.lidDown", "edo.coinTraded", "edo.funadamaList", "edo.chirped",      // #27 Don't Lift The Lid
  "edo.sailed"];                                                                                            // The Uttermost Parts
// SCENES-21B: Osaka's and the hills' lists made whole: every fact the leg's scenes and talks set on the way, in the order they are
// set (the scenes' own and the trees': edo-dojima.js, edo-street.js, edo-theatre.js, cutscenes/edo-boat.js; the hills as round
// twenty built them, less the two that are true only for a moment and false by the leg's end: edo.isukeIn, edo.crossShown, and
// edo.mirrorUp, which the walk card lets go)
const OSAKA = ["edo.landed", "edo.natsuMet", "edo.paddle", "edo.potServed", "edo.ballsShaped", "edo.pickleServed", "edo.fifthCaught",
  "edo.fedPilgrims", "edo.vouched", "edo.supped",                                                            // #28 The Dōjima Shore
  "edo.streetSeen", "edo.combAsked", "edo.heardShosha", "edo.sheetCaught", "edo.followed", "edo.combGiven", // #29 What The Road God Said
  "edo.senzoMet", "edo.marksSeen", "edo.registered", "edo.sheetRead",                                       // #30 Berlin Blue
  "edo.backstage", "edo.jubeiMet", "edo.ruleHeard", "edo.hooded", "edo.rehearsedLeft", "edo.rehearsedFeet", "edo.rehearsed",
  "edo.momSeated", "edo.cue1", "edo.cue2", "edo.cue3", "edo.troupeTaken",                                   // #31 Three To A Puppet
  "edo.boated"];                                                                                            // The Kyoto Boat
const HILLS = ["edo.cedarsSeen", "edo.pipeHeard", "edo.unbarred", "edo.matMoved", "edo.knocked", "edo.hidden",      // #32 (round twenty's #25)
  "edo.roomMet", "edo.prayed", "edo.altarOpen", "edo.verse", "edo.laughed", "edo.trusted",                  // #33
  "edo.lightLeft", "edo.watch", "edo.momBelow", "edo.sacksHid", "edo.pinkOff", "edo.isukeAtDoor", "edo.eggGiven", "edo.constableGone",
  "edo.mirror",                                                                                             // #34
  "edo.walked"];                                                                                            // Three days later
// SCENES-21C: the facts the Akashi shore, Himeji town, Shosha and the hall set, in the order a game played through sets them
// (the scenes' and the trees'; the stage facts acts/edo.js reads are among them, by those names)
const AKASHI = ["edo.akashiSeen", "edo.fusaMet", "edo.heitaMet", "edo.waded", "edo.crabClue", "edo.tako", "edo.crab", "edo.ladleFree",   // #35 The Ladle
  "edo.ladleBack", "edo.satoMet", "edo.riddle",
  "edo.inHimeji"];                                                                                          // The next day
const TOWN = ["edo.taneMet", "edo.kikuIn", "edo.shizuThanked", "edo.knowWay", "edo.tobeiMet", "edo.kitchenLent",                    // #36 Supper For A Voice
  "edo.cook.water", "edo.cook.salt", "edo.cook.rice", "edo.cook.plum", "edo.cook.pickle", "edo.riceballs", "edo.taneBed", "edo.supperMade",
  "edo.umeGreeted", "edo.oumeMet", "edo.ryokaiMet", "edo.tomeMet", "edo.natsuGiven", "edo.fusaGiven", "edo.lockSeen", "edo.listRead",   // #37 What A Ship Gives Its Lady
  "edo.earClean", "edo.hallOpen", "edo.umeIn",
  "edo.tomeHome", "edo.sonHeard", "edo.eatenAsked", "edo.doorWide", "edo.sonFed", "edo.holdHands",          // #38 A Small Door At Sunset
  "edo.nightDone"];                                                                                         // Mind The Fire
export const LEG_START = {
  yui: { scene: "edo-village", spawn: "arrive", flags: ["office.done"], outfit: null,
    pockets: { mom: ["carkey"], bigsis: ["pencil", "note", "coin"], lilsis: ["pennies", "egg", "lilflash"] } },      // SCENES-21A: the pockets as Act Four left them (was bigsis coin; lilsis egg, lilflash: no pennies for #23 and #27)
  // ENGINE-21: on deck, the fifth day out (after Casting Off): Big Sister has O-Tami's hairpin, Little Sister her three pennies
  // and Sōshichi's print; the box of sushi is eaten
  deck: { scene: "edo-deck", spawn: "deck", outfit: "edo", flags: [...YUI, ...CASTOFF],
    pockets: { mom: ["carkey"], bigsis: ["pencil", "note", "coin", "kanzashi"], lilsis: ["pennies", "lilflash", "egg", "toyamaprint"] } },
  // ENGINE-21: Osaka, landed on the Dōjima shore: a penny for Kōta's coin (two pennies; the one-mon coin). (SCENES-21B: the
  // moment edo-dojima comes up on `landing`, before its landing plays: the lighter still at the steps)
  osaka: { scene: "edo-dojima", spawn: "landing", outfit: "edo", flags: [...YUI, ...CASTOFF, ...DECK],
    pockets: { mom: ["carkey"], bigsis: ["pencil", "note", "coin", "kanzashi"], lilsis: ["twopennies", "mon", "lilflash", "egg", "toyamaprint"] } },
  // ENGINE-21: the hills, by the Kyoto boat (was: by "go north" after the voyage): O-Natsu's comb and slip, the broadsheet, the
  // spoiled blue print (SCENES-21B: the paddle given back at the supper; the three in their travel clothes, hats on for the rain)
  hills: { scene: "edo-cedars", spawn: "enter", outfit: "edo", flags: [...YUI, ...CASTOFF, ...DECK, ...OSAKA],
    pockets: { mom: ["carkey", "comb", "natsuslip"], bigsis: ["pencil", "note", "coin", "kanzashi", "sheet"], lilsis: ["twopennies", "mon", "lilflash", "egg", "toyamaprint", "blueprint"] } },
  // ENGINE-21: the Akashi shore, three days later: the bronze mirror and the trowel (as built); the egg given
  akashi: { scene: "edo-akashi", spawn: "road", outfit: "edo", flags: [...YUI, ...CASTOFF, ...DECK, ...OSAKA, ...HILLS],
    pockets: { mom: ["carkey", "comb", "natsuslip", "mirror", "trowel"], bigsis: ["pencil", "note", "coin", "kanzashi", "sheet"], lilsis: ["twopennies", "mon", "lilflash", "toyamaprint", "blueprint"] } },
  // ENGINE-21: Himeji town, the next day: a penny for luck (the last penny), O-Fusa's slip
  town: { scene: "edo-town", spawn: "east", outfit: "edo", flags: [...YUI, ...CASTOFF, ...DECK, ...OSAKA, ...HILLS, ...AKASHI],
    pockets: { mom: ["carkey", "comb", "natsuslip", "mirror", "trowel"], bigsis: ["pencil", "note", "coin", "kanzashi", "sheet"], lilsis: ["lastpenny", "mon", "lilflash", "toyamaprint", "blueprint", "fusaslip"] } },
  // ENGINE-21: the castle, the day after Shosha (was: three days after the hills): the slips and the coin left with O-Ume, the comb
  // and the pin back; the rice ball for the Son waits in the tunnel
  himeji: { scene: "edo-castle", spawn: "enter", outfit: "edo", flags: [...YUI, ...CASTOFF, ...DECK, ...OSAKA, ...HILLS, ...AKASHI, ...TOWN],
    pockets: { mom: ["carkey", "comb", "mirror", "trowel"], bigsis: ["pencil", "note", "coin", "kanzashi", "sheet"], lilsis: ["lastpenny", "lilflash", "toyamaprint", "blueprint"] },
    tunnel: [{ item: "riceball", from: "mom", to: "son" }] },
};

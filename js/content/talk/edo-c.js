// The talks of Act Six made bigger, column A: the road over the Satta Pass, the ship by day, Osaka (WRITE-21A: new in round
// twenty-one; briefs/WRITE-21.md, and the design, briefs/out/edo2-design.md, section 7, #24 to #31). Plain data in the
// engine's format (docs/DESIGN.md, section 7, "Dialogue trees"), made as round twenty's talk/edo-a.js makes them: every word
// is a line id (js/content/lines/edo-c.en.js). An option's `line` is said by the one it belongs to (Mom, Big Sister or
// Little Sister: the three are a team, all on stage, so a menu may mix their lines); its `say` is the reply; `set` makes
// facts true; `then` goes to a node, "back", "root" or "exit" (or is a function of the game giving one). TALK-18's rule
// holds: a picked option is gone unless it is a clue (`clue: true`), a way out, or `keep`.
//
// Each tree is a function of a `hooks` object, so that the scene hands in the scripts a branch needs:
//     import { kotaTree } from "../talk/edo-c.js";
//     const KOTA = kotaTree({ wait, serve, look, trade, chirp });
//     ...  use: (g) => g.talk(KOTA)
// A hook that is not handed in is passed over (the talk still says every line and sets every fact).
//
// THE HOOKS, and what each must do. None says a line the tree says.
//   kuniTree (O-Kuni at her grill, Nishikurasawa)
//     shell(g)      she hands over one turban shell, hot, on a leaf; the three share it (staging). (edo.shellShared after.)
//   bearersTree (Sakuji and Tora on their pole by the mound)
//     sit(g)        Little Sister climbs into the palanquin, sits, bounces a very little, and climbs out. Staging.
//   soshichiTree (Sōshichi by his trunks)
//     print(g)      he takes a print from the second tier and gives it: g.give("toyamaprint") to Little Sister (whoever is
//                   talking; the tree only offers it to her). (edo.printGiven after.)
//   shigeTree (O-Shige on her stone at the top of the pass, Kyūzō beside her with the box)
//     giveBack(g)   the pass handed back to her: the lead's `shigepass` taken (g.take, if the scene made it an item); she
//                   goes white, then pink, and sits down on her stone. (edo.passBack after the lines.)
//     clears(g)     the cloud lifts off Fuji (the scene fades the cap: ENGINE-21's layer fade). (edo.fujiClear after.)
//     shore(g)      they look down at the old shore under the cliffs (staging; the waves white below).
//   mosukeTree (Mosuke the woodcutter on the road, his load on his back)
//     pole(g)       he lends his load pole to whoever asked: the paper can be lifted off the Jizō's hat with it without
//                   touching him (the scene's use of `pass` with the pole: edo.satta.pass.pole.<who>). (edo.poleLent after.)
//   kanbeiTree (Kanbei at the compass box by the tiller, on deck)
//     closeup(g)    the compass close-up opens (edo-compass): Big Sister's first look at the needle there is the
//                   working-out (the scene says edo.compass.first.1 to .7 and sets edo.compassRead).
//     freeze(g)     after "Saru.": the whole crew freezes, Denzō's hand on the mast, the windlass men stock-still, a gull
//                   overhead. Staging. (edo.saruSaid after the lines.)
//     hold(g)       after the call: the tiller over a hair, the sail settling, the ship holding for the Kumano-nada.
//                   Staging and sound. (edo.headingCalled after: the beat of #26.)
//   denzoTree (Denzō by the mast)
//     write(g)      Big Sister writes the list on the sticky note in Dad's pencil (her pose; she must be holding the note:
//                   world.js `note` reads item.note.list.<who> from edo.funadamaList on). (edo.funadamaList after.)
//     chirp(g)      the chirp, if this was the last of #27's four: Kōta laughs (his pose), and from the foot of the mast two
//                   small bright notes (ENGINE-21's chirp sound). (edo.chirped after the lines.)
//   kotaTree (Kōta at his hearth box)
//     wait(g)       after Mom's lesson: the lid stays on; Kōta's hands hover; the pot crackles (between the wait lines the
//                   tree says, edo.deck.wait.1 to .8: the hook is called before them and may stage them as it likes).
//     serve(g)      the rice off the fire and into bowls; the crew eat (the two sailors, Denzō, Gonroku at the tiller).
//                   (edo.lidDown after the lines.)
//     look(g)       Little Sister looks at her three pennies a long time (a held pose, a silence).
//     trade(g)      the trade: g.take("pennies"), g.give("twopennies"), g.give("mon"), all Little Sister's; Kōta's hand
//                   closes on his penny. (edo.coinTraded after the lines.)
//     chirp(g)      as denzoTree's, when the lid or the coin was the last of the four.
//   gonrokuDeckTree (Gonroku at the tiller): no hooks.
//   natsuTree (O-Natsu at her alms stall on the Dōjima shore)
//     paddle(g)     she hands Mom her rice paddle: g.give("paddle") to Mom (Mom's hold `paddle`). (edo.paddle after.)
//     sit(g)        the helpers sit on the river steps with the last of the pot (their supper). Staging.
//     eat(g)        after Little Sister's grace: they eat (bowls, rice balls; no table word). Staging.
//     giveBack(g)   Mom gives the paddle back, clean: g.take("paddle"). (edo.supped after the lines.)
//   riheiTree, kyuhachiTree: no hooks.
//   natsuStreetTree (O-Natsu at the crossroads on Shinsaibashi-suji)
//     pray(g)       Mom, beside her, bows her head and folds her hands (actor.pray), while O-Natsu holds up her comb.
//     sellers(g)    the yomiuri pair come round the corner, chanting (yomiuri1, yomiuri2 walk in to the crossroads).
//     men(g)        Kurata and Tatsu round the other corner; the pair run off the right edge; a sheet flutters down and Big
//                   Sister has it before it lands: g.give("sheet") to her. Tatsu stays, looking. (edo.sheetCaught and
//                   edo.followed after the lines: the theater's way opens.)
//     gift(g)       she presses the comb into Mom's hands, and then the slip: g.give("comb"), g.give("natsuslip"), Mom's.
//                   (edo.combGiven after the lines.)
//   senzoTree (Senzō at his bench in the print shop's open front)
//     watch(g)      he prints one sheet by eye while Big Sister watches (the blue a hair to the left). Staging; the laying
//                   itself is the scene's three hotspots (edo.senzo.lay.*: corner mark, side mark, his rub).
//     curtain(g)    he draws the shop's curtain a little across the front before he reads. Staging.
//   jubeiTree (Jūbei backstage at the Inari theater, the boy puppet on its stand)
//     robes(g)      the girls into the black robes and hoods: g.dress("bigsis", "edo-kurogo"), g.dress("lilsis",
//                   "edo-kurogo") (PEOPLE-21B's outfit; Little Sister's boots showing). (edo.hooded after.)
//     practise(g)   the girl whose part it is tries it once on the stand (the puppet's pose: `ear` for the left hand, `run`
//                   for the feet). Staging.
//
// THE FACTS. Set by the trees: edo.kuniMet, edo.shellShared, edo.araiWarned (she has said papers at Arai), edo.kuniBack,
// edo.bearersMet, edo.bearersBack, edo.soshichiMet, edo.printGiven, edo.soshichiBack, edo.shigeMet, edo.passBack,
// edo.araiHeard, edo.fujiClear, edo.oldShoreHeard, edo.noRoad (#24's beat), edo.mosukeMet, edo.poleLent, edo.kanbeiMet,
// edo.englishTried, edo.saruSaid, edo.headingCalled (#26's beat), edo.denzoMet, edo.funadamaList, edo.seaWords,
// edo.kotaMet, edo.saruHeard, edo.lidDown, edo.coinTraded, edo.chirped (#27's beat), edo.natsuMet, edo.paddle, edo.supped,
// edo.combAsked, edo.heardShosha (#29's beat fact), edo.sheetCaught, edo.followed, edo.combGiven, edo.senzoMet,
// edo.marksSeen, edo.sheetRead (#30's beat fact), edo.jubeiMet, edo.ruleHeard, edo.hooded, edo.rehearsedLeft,
// edo.rehearsedFeet, edo.rehearsed, edo.troupeTaken (#31's beat fact). Set by the scenes, and read here: edo.gust (the pass
// blown onto the Jizō: at the top, the first time), edo.passFound (lifted off), edo.compassRead (the working-out in the
// close-up), edo.fedPilgrims (the line fed: the three tasks done), edo.vouched ("My helpers."), edo.registered (the laying
// in order), edo.momSeated, edo.cue1, edo.cue2, edo.cue3 (the show). And g.has(...) (the one talking has it),
// g.asked("<tree>/<option>"), the lines heard (g.store.data.seenLines). S/work-21-writeA/ids.md says when each is said.
//
// Besides the trees, the sequences the cut-scenes and the scenes' scripted moments say, in order (as round twenty's WALK and
// STEP): CASTOFF, SAIL_EDIT, BOAT, LIST, VOUCH, FIFTH, SHOW, SEAT, AFTER_SHOW, LAY, CHIRP.

import { topic, back } from "./topics.js";      // TALK-24: topics, and the way back out of one

const who = (g) => g.store.data.active;
const is = (g, fact) => !!g.flag(fact);
const lead = (g) => (["mom", "bigsis", "lilsis"].includes(who(g)) ? who(g) : "mom");
const node = (g) => ({ mom: "mom", bigsis: "big", lilsis: "lil" }[lead(g)]);
const heard = (g, id) => !!((g.store.data.seenLines || {})[id]);
const run = async (h, name, g) => { if (h[name]) await h[name](g); };
/** A way out for each of the three, in her own node. */
const bye = (id, line, say) => ({ id, line, say, then: "exit" });

// ======================================================================================================
// THE SEQUENCES (for the cut-scenes and the scenes' scripted moments: a list of line ids in the order said; the staging
// between them is the design's and ids.md's)
// ======================================================================================================
/** Casting Off (edo-castoff.js): after round twenty's goodbyes (edo.west.bye.1 to .10): O-Masa at the boat; the ship's boat;
    the windlass; the sail; the purser; Gonroku; then the first night (round twenty's box: edo.sail.box.1, .2); the card. */
export const CASTOFF = ["edo.card.castoff.title", "edo.castoff.masa.1", "edo.castoff.masa.2", "edo.castoff.masa.3",
  "edo.castoff.boat.1", "edo.castoff.boat.2", "edo.castoff.boat.3", "edo.castoff.heave.1", "edo.castoff.heave.2",
  "edo.castoff.heave.1", "edo.castoff.heave.2", "edo.castoff.heave.3", "edo.castoff.sail.1", "edo.castoff.sail.2",
  "edo.castoff.sail.3", "edo.castoff.sail.4", "edo.castoff.count.1", "edo.castoff.count.2", "edo.castoff.count.3",
  "edo.castoff.gonroku", "edo.sail.box.1", "edo.sail.box.2", "edo.card.castoff.later"];
/** The Uttermost Parts, the new part after the night and the psalm (round twenty's edo.sail.1, .2, .4 to .7): the card
    (edo.card.sail.later, or round twenty's edo.card.sail: ready.md), Osaka, the river mouth, the lighter, the goodbye. */
export const SAIL_EDIT = ["edo.card.sail.later", "edo.card.osaka", "edo.sail.mouth.1", "edo.sail.mouth.2", "edo.sail.mouth.3",
  "edo.sail.mouth.4", "edo.sail.lighter.1", "edo.sail.lighter.2", "edo.sail.lighter.3", "edo.sail.lighter.4",
  "edo.sail.osaka.3", "edo.sail.osaka.3b", "edo.sail.osaka.4", "edo.sail.bye.1", "edo.sail.bye.2", "edo.sail.osaka.5"];
/** The landing at the Dōjima steps (the deck's last: the scene, on the mark `landing`, as the lighter pulls away). */
export const LANDING = ["edo.dojima.arrive.1", "edo.dojima.arrive.2", "edo.dojima.arrive.3"];
/** The Kyoto Boat (edo-boat.js). */
export const BOAT = ["edo.card.boat.title", "edo.boat.1", "edo.boat.2", "edo.boat.3", "edo.boat.4", "edo.boat.5", "edo.boat.6",
  "edo.boat.7", "edo.boat.8", "edo.boat.9", "edo.boat.10", "edo.boat.11", "edo.boat.12", "edo.boat.13", "edo.boat.14",
  "edo.boat.15", "edo.boat.16", "edo.boat.17", "edo.card.boat.hills"];
/** What the Funadama was given (Denzō's, at the first knock on the mast step or asked in his tree; edo.funadamaList). */
export const LIST = ["edo.denzo.list.1", "edo.denzo.list.2", "edo.denzo.list.3", "edo.denzo.list.4", "edo.denzo.list.5", "edo.denzo.list.6"];      // (WRITE-25)
/** The chirp (after the laugh's lead-in line: edo.deck.chirp.coin, .lid or .list). */
export const CHIRP = ["edo.deck.chirp.0", "edo.deck.chirp.1", "edo.deck.chirp.2", "edo.deck.chirp.3", "edo.deck.chirp.4", "edo.deck.chirp.5"];      // (WRITE-25: the narrator first, for the sound)
/** #28: the line fed (edo.fedPilgrims), then Kurata along it ("My helpers.": edo.vouched). */
export const VOUCH = ["edo.dojima.fed.1", "edo.dojima.vouch.1", "edo.dojima.vouch.2", "edo.dojima.vouch.3", "edo.dojima.vouch.4", "edo.dojima.vouch.5"];
/** #28: Kyūhachi at Little Sister's tub, the fifth time. */
export const FIFTH = ["edo.dojima.fifth.1", "edo.dojima.fifth.2", "edo.dojima.fifth.3", "edo.dojima.fifth.4"];
/** #30: the laying, in order (the three hotspots say one each), and its two ends. */
export const LAY = { corner: "edo.senzo.lay.corner", side: "edo.senzo.lay.side", rub: "edo.senzo.lay.rub",
  good: ["edo.senzo.lay.good.1", "edo.senzo.lay.good.2", "edo.senzo.lay.good.3"],
  ghost: ["edo.senzo.lay.ghost.1", "edo.senzo.lay.ghost.2", "edo.senzo.lay.ghost.3"], again: "edo.senzo.lay.again",
  rubFirst: "edo.senzo.lay.rubfirst", sideFirst: "edo.senzo.lay.sidefirst" };
/** #31: Mom out front, and her seat beside Tatsu (edo.momSeated). */
export const SEAT = ["edo.theatre.mom.1", "edo.theatre.seat.1", "edo.theatre.seat.2", "edo.theatre.seat.3", "edo.theatre.seat.4",
  "edo.theatre.seat.5", "edo.theatre.seat.6"];
/** #31: the show. Each cue waits for its part (cue1: Big Sister's left hand to the ear; cue2: Little Sister's stamping run;
    cue3: both, the hand to the ground and the feet folded); a part at the wrong cue: the audience laughs, `wrong`, and the
    cue is said again. */
export const SHOW = { open: "edo.chanter.open", cues: ["edo.chanter.cue1", "edo.chanter.cue2", "edo.chanter.cue3"],
  wrong: ["edo.jubei.notyet", "edo.jubei.notyet.2"], end: "edo.chanter.end",
  after: ["edo.theatre.after.1", "edo.theatre.after.2", "edo.theatre.after.3"] };

// ======================================================================================================
// THE ROAD (#24): Nishikurasawa and the top of the Satta Pass
// ======================================================================================================
/** kuniTree: O-Kuni, the teahouse woman. She sells while she warns: the shell, for the climb; "And your pass?"; Arai. */
export const kuniTree = (h = {}) => {
  const west = (id, line) => ({ id, line, clue: true, when: (g) => !is(g, "edo.araiWarned"), then: "pass" });
  return {
    id: "kuni",
    start: (g) => (!is(g, "edo.kuniMet") ? "first" : is(g, "edo.noRoad") && !is(g, "edo.kuniBack") ? "back" : node(g)),
    nodes: {
      first: { say: ["edo.kuni.cry", "edo.kuni.open"], then: (g) => { g.flag("edo.kuniMet", true); return node(g); } },
      mom: {
        options: [
          { id: "morningMom", line: "edo.kuni.opt.morning.mom", when: (g) => !is(g, "edo.shellShared"), say: ["edo.kuni.morning.1"], then: "gift" },
          west("westMom", "edo.kuni.opt.west.mom"),
          { id: "fujiMom", line: "edo.kuni.opt.fuji.mom", once: true, when: (g) => !is(g, "edo.fujiClear"), say: ["edo.kuni.fuji.1"] },
          { id: "backMom", line: "edo.kuni.opt.back.mom", once: true, when: (g) => is(g, "edo.noRoad"), say: ["edo.kuni.back.mom"] },
          bye("byeMom", "edo.kuni.opt.bye.mom", ["edo.kuni.bye.mom"]),
        ],
      },
      big: {
        options: [
          { id: "signBig", line: "edo.kuni.opt.sign.big", once: true, say: ["edo.kuni.sign.big"] },
          west("westBig", "edo.kuni.opt.west.big"),
          { id: "thirtyBig", line: "edo.kuni.opt.thirty.big", once: true, say: ["edo.kuni.thirty.big"] },
          bye("byeBig", "edo.kuni.opt.bye.big", ["edo.kuni.bye.big"]),
        ],
      },
      lil: {
        options: [
          { id: "shellLil", line: "edo.kuni.opt.shell.lil", when: (g) => !is(g, "edo.shellShared"), say: ["edo.kuni.shell.lil"], then: "gift" },
          west("westLil", "edo.kuni.opt.west.lil"),
          { id: "fujiLil", line: "edo.kuni.opt.fuji.lil", once: true, when: (g) => !is(g, "edo.fujiClear"), say: ["edo.kuni.fuji.lil", "edo.kuni.fuji.1"] },
          { id: "hissLil", line: "edo.kuni.opt.hiss.lil", once: true, say: ["edo.kuni.hiss.lil"] },
          { id: "backLil", line: "edo.kuni.opt.back.lil", once: true, when: (g) => is(g, "edo.noRoad") && is(g, "edo.fujiClear"), say: ["edo.kuni.back.lil"] },
          bye("byeLil", "edo.kuni.opt.bye.lil", ["edo.kuni.bye.lil"]),
        ],
      },
      // the shell, for the climb (Little Sister thanks her with the word, if she has it from Sankichi)
      gift: { say: ["edo.kuni.gift.1"], then: async (g) => { await run(h, "shell", g); return "shared"; } },
      shared: { say: ["edo.kuni.gift.2", "edo.kuni.gift.3", "edo.kuni.gift.4"], then: (g) => (is(g, "edo.arigato") ? "thanksWord" : "thanksPlain") },
      thanksWord: { say: ["edo.kuni.gift.5", "edo.kuni.gift.6"], then: (g) => { g.flag("edo.shellShared", true); return "root"; } },
      thanksPlain: { say: ["edo.kuni.gift.5b", "edo.kuni.gift.6"], then: (g) => { g.flag("edo.shellShared", true); return "root"; } },
      // where they are going; "And your pass?"; Arai, said once (edo.araiWarned)
      pass: { say: ["edo.kuni.west.1", "edo.kuni.pass.1", "edo.kuni.pass.2", "edo.kuni.pass.3", "edo.kuni.pass.4", "edo.kuni.pass.5",
        "edo.kuni.pass.6", "edo.kuni.pass.mom"], then: (g) => { g.flag("edo.araiWarned", true); return "root"; } },
      // back down from the top (said once)
      back: { say: ["edo.kuni.back"], then: (g) => { g.flag("edo.kuniBack", true); return node(g); } },
    },
  };
};

/** bearersTree: Sakuji and Tora, the palanquin bearers. They bargain before anyone has asked. Nobody has money. */
export const bearersTree = (h = {}) => ({
  id: "bearers",
  start: (g) => (!is(g, "edo.bearersMet") ? "first" : is(g, "edo.noRoad") && !is(g, "edo.bearersBack") ? "back" : node(g)),
  nodes: {
    first: { say: ["edo.bearers.open.1", "edo.bearers.open.2"], then: (g) => { g.flag("edo.bearersMet", true); return node(g); } },
    mom: {
      options: [
        { id: "fareMom", line: "edo.bearers.opt.fare.mom", once: true, say: ["edo.bearers.fare.mom.1", "edo.bearers.fare.mom.2", "edo.bearers.fare.mom.3"] },
        { id: "toraMom", line: "edo.bearers.opt.tora.mom", once: true, say: ["edo.bearers.tora.mom.1", "edo.bearers.tora.mom.2"] },
        bye("byeMom", "edo.bearers.opt.bye.mom", ["edo.bearers.bye.mom"]),
      ],
    },
    big: {
      options: [
        { id: "fareBig", line: "edo.bearers.opt.fare.big", once: true, say: ["edo.bearers.fare.big.1", "edo.bearers.fare.big.2"] },
        { id: "drinkBig", line: "edo.bearers.opt.drink.big", once: true, say: ["edo.bearers.drink.big.1", "edo.bearers.drink.big.2"] },
        bye("byeBig", "edo.bearers.opt.bye.big", ["edo.bearers.bye.big"]),
      ],
    },
    lil: {
      options: [
        // the ride: "How much have you got?" "Three pennies." (she has three until #27)
        { id: "rideLil", line: "edo.bearers.opt.ride.lil", once: true, when: (g) => g.has("pennies"),
          say: ["edo.bearers.ride.1", "edo.bearers.ride.2", "edo.bearers.ride.3", "edo.bearers.ride.4", "edo.bearers.ride.5", "edo.bearers.ride.6", "edo.bearers.ride.7"] },
        { id: "sitLil", line: "edo.bearers.opt.sit.lil", once: true, say: ["edo.bearers.sit.1", "edo.bearers.sit.2"], then: "sat" },
        bye("byeLil", "edo.bearers.opt.bye.lil", ["edo.bearers.bye.lil"]),
      ],
    },
    sat: { then: async (g) => { await run(h, "sit", g); return "satDone"; } },
    satDone: { say: ["edo.bearers.sit.3"], then: "lil" },
    back: { say: ["edo.bearers.back", "edo.bearers.back.2"], then: (g) => { g.flag("edo.bearersBack", true); return node(g); } },
  },
});

/** soshichiTree: Sōshichi, the Toyama medicine peddler. Use first, pay later; he counts; a print for the child. */
export const soshichiTree = (h = {}) => {
  const road = (id, line) => ({ id, line, clue: true, when: (g) => !is(g, "edo.noRoad"), say: ["edo.soshichi.road.1", "edo.soshichi.road.2"] });
  return {
    id: "soshichi",
    start: (g) => (!is(g, "edo.soshichiMet") ? "first" : is(g, "edo.noRoad") && !is(g, "edo.soshichiBack") ? "back" : node(g)),
    nodes: {
      first: { say: ["edo.soshichi.open"], then: (g) => { g.flag("edo.soshichiMet", true); return node(g); } },
      mom: {
        options: [
          { id: "trustMom", line: "edo.soshichi.opt.trust.mom", once: true, say: ["edo.soshichi.trust.1", "edo.soshichi.trust.2"] },
          road("roadMom", "edo.soshichi.opt.road.mom"),
          { id: "printThanksMom", line: "edo.soshichi.opt.printthanks.mom", once: true, when: (g) => is(g, "edo.printGiven"), say: ["edo.soshichi.printthanks.mom"] },
          bye("byeMom", "edo.soshichi.opt.bye.mom", ["edo.soshichi.bye.mom"]),
        ],
      },
      big: {
        options: [
          { id: "ledgerBig", line: "edo.soshichi.opt.ledger.big", once: true, say: ["edo.soshichi.ledger.1", "edo.soshichi.ledger.2", "edo.soshichi.ledger.3"] },
          road("roadBig", "edo.soshichi.opt.road.big"),
          bye("byeBig", "edo.soshichi.opt.bye.big", ["edo.soshichi.bye.big"]),
        ],
      },
      lil: {
        options: [
          { id: "boxesLil", line: "edo.soshichi.opt.boxes.lil", once: true, say: ["edo.soshichi.boxes.1", "edo.soshichi.boxes.2"],
            then: (g) => (is(g, "edo.printGiven") ? null : "print") },
          { id: "farLil", line: "edo.soshichi.opt.far.lil", once: true, say: ["edo.soshichi.far.lil"] },
          bye("byeLil", "edo.soshichi.opt.bye.lil", ["edo.soshichi.bye.lil"]),
        ],
      },
      // the print, for the child (toyamaprint)
      print: { say: ["edo.soshichi.print.1", "edo.soshichi.print.2", "edo.soshichi.print.3"],
        then: async (g) => { await run(h, "print", g); g.flag("edo.printGiven", true); return "printed"; } },
      printed: { say: ["edo.soshichi.print.4", "edo.soshichi.print.5"], then: "lil" },
      back: { say: ["edo.soshichi.back"], then: (g) => { g.flag("edo.soshichiBack", true); return node(g); } },
    },
  };
};

/** shigeTree: O-Shige, on her stone at the top. Her pass, given back (edo.passBack); then the truth about Arai, told kindly
    (edo.araiHeard); the cloud lifts off Fuji (edo.fujiClear); the old shore's name (edo.oldShoreHeard, unless Mosuke has
    told it); "Nobody's forgetting anybody." (edo.noRoad: the beat of #24). */
export const shigeTree = (h = {}) => {
  const back = (id, line, to) => ({ id, line, when: (g) => is(g, "edo.passFound") && !is(g, "edo.passBack"), then: to });
  const west = (id, line) => ({ id, line, when: (g) => is(g, "edo.passBack") && !is(g, "edo.araiHeard"), then: "arai" });
  const ARAI = ["edo.shige.arai.1", "edo.shige.arai.2", "edo.shige.arai.3", "edo.shige.arai.4", "edo.shige.arai.5", "edo.shige.arai.6",
    "edo.shige.arai.7", "edo.shige.arai.8", "edo.shige.arai.9", "edo.shige.arai.10"];
  const handOver = (next) => async (g) => { await run(h, "giveBack", g); return next; };
  const moleNext = (g) => (heard(g, "edo.satta.passuse.1") ? "mole8" : "mole9");
  return {
    id: "shige",
    start: (g) => (is(g, "edo.noRoad") ? "after" : is(g, "edo.passBack") ? (is(g, "edo.araiHeard") ? "after" : "sitdown") : is(g, "edo.shigeMet") ? node(g) : "first"),
    nodes: {
      first: { say: ["edo.shige.first"], then: (g) => { g.flag("edo.shigeMet", true); return node(g); } },
      sitdown: { say: ["edo.shige.back"], then: node },
      mom: {
        options: [
          back("backMom", "edo.satta.back.1", "givingMom"),
          west("westMom", "edo.shige.opt.west.mom"),
          { id: "climbMom", line: "edo.shige.opt.climb.mom", once: true, say: ["edo.shige.climb.mom"] },
          bye("byeMom", "edo.shige.opt.bye.mom", ["edo.shige.bye.mom"]),
        ],
      },
      big: {
        options: [
          back("backBig", "edo.satta.back.1.big", "givingBig"),
          west("westBig", "edo.shige.opt.west.big"),
          { id: "paperBig", line: "edo.shige.opt.paper.big", once: true, say: ["edo.shige.paper.big"] },
          bye("byeBig", "edo.shige.opt.bye.big", ["edo.shige.bye.big"]),
        ],
      },
      lil: {
        options: [
          back("backLil", "edo.satta.back.1.lil", "givingLil"),
          west("westLil", "edo.shige.opt.west.lil"),
          { id: "whereLil", line: "edo.shige.opt.where.lil", once: true, say: ["edo.shige.where.1", "edo.shige.where.2"] },
          { id: "kyuzoLil", line: "edo.shige.opt.kyuzo.lil", once: true, say: ["edo.shige.kyuzo.1", "edo.shige.kyuzo.2"] },
          bye("byeLil", "edo.shige.opt.bye.lil", ["edo.shige.bye.lil"]),
        ],
      },
      // the pass given back: by whoever has it; she goes white, then pink, and sits down on her stone
      givingMom: { say: ["edo.satta.back.2", "edo.satta.back.3", "edo.satta.back.4"], then: handOver("gaveMom") },
      givingBig: { say: ["edo.satta.back.2", "edo.satta.back.3", "edo.satta.back.4"], then: handOver("gaveBig") },
      givingLil: { say: ["edo.satta.back.2", "edo.satta.back.3", "edo.satta.back.4"], then: handOver("gaveLil") },
      gaveMom: { say: ["edo.satta.back.5", "edo.satta.back.6"], then: moleNext },
      gaveBig: { say: ["edo.satta.back.5", "edo.satta.back.6.big"], then: moleNext },
      gaveLil: { say: ["edo.satta.back.5", "edo.satta.back.6.lil"], then: moleNext },
      // the description on it (Big Sister's "...Mom." only if Mom has said what she thought it said)
      mole8: { say: ["edo.satta.back.7", "edo.satta.back.8", "edo.satta.back.9"], then: (g) => { g.flag("edo.passBack", true); return "sitdown"; } },
      mole9: { say: ["edo.satta.back.7", "edo.satta.back.9"], then: (g) => { g.flag("edo.passBack", true); return "sitdown"; } },
      // Arai, told kindly; "Then not by road."; "Find a captain."; the cloud lifts; the old shore; Mom's word
      arai: { say: ARAI, then: (g) => { g.flag("edo.araiHeard", true); return "captain"; } },
      captain: { say: ["edo.shige.arai.11"], then: async (g) => { await run(h, "clears", g); g.flag("edo.fujiClear", true); return "cleared"; } },
      cleared: { say: ["edo.satta.clears.1", "edo.satta.clears.2", "edo.satta.clears.3"], then: (g) => (is(g, "edo.oldShoreHeard") ? "noroad" : "shore") },
      shore: { then: async (g) => { await run(h, "shore", g); return "named"; } },
      named: { say: ["edo.satta.name.shige.1", "edo.satta.name.shige.2", "edo.satta.name.3"], then: (g) => { g.flag("edo.oldShoreHeard", true); return "noroad"; } },
      noroad: { say: ["edo.satta.noroad"], then: (g) => { g.flag("edo.noRoad", true); return "exit"; } },
      // after: her last word, and the goodbyes (the scene sends her on down east)
      after: {
        say: ["edo.shige.after"],
        options: [
          { id: "thanksMom", line: "edo.shige.opt.thanks.mom", once: true, say: ["edo.shige.thanks.mom"] },
          bye("afterByeLil", "edo.shige.opt.bye.lil", ["edo.shige.bye.lil"]),
          bye("afterByeBig", "edo.shige.opt.bye.big", ["edo.shige.bye.big"]),
          bye("afterByeMom", "edo.shige.opt.bye.mom", ["edo.shige.bye.mom"]),
        ],
      },
    },
  };
};

/** mosukeTree: Mosuke, the woodcutter who never looks at Fuji. "Seen it." The old shore's name; his pole. */
export const mosukeTree = (h = {}) => {
  const shore = (id, line) => ({ id, line, once: true, when: (g) => !is(g, "edo.oldShoreHeard"), then: "shore" });
  const pole = (id, line) => ({ id, line, when: (g) => is(g, "edo.gust") && !is(g, "edo.passFound") && !is(g, "edo.poleLent"), then: "pole" });
  return {
    id: "mosuke",
    start: (g) => (is(g, "edo.mosukeMet") ? node(g) : "first"),
    nodes: {
      first: { say: ["edo.mosuke.open"], then: (g) => { g.flag("edo.mosukeMet", true); return node(g); } },
      mom: {
        options: [
          { id: "everyMom", line: "edo.mosuke.opt.every.mom", once: true, say: ["edo.mosuke.every.mom"] },
          shore("shoreMom", "edo.mosuke.opt.shore.mom"),
          pole("poleMom", "edo.mosuke.opt.pole.mom"),
          bye("byeMom", "edo.mosuke.opt.bye.mom", ["edo.mosuke.bye"]),
        ],
      },
      big: {
        options: [
          { id: "nameBig", line: "edo.mosuke.opt.name.big", once: true, say: ["edo.mosuke.name.big"] },
          shore("shoreBig", "edo.mosuke.opt.shore.big"),
          pole("poleBig", "edo.mosuke.opt.pole.big"),
          { id: "okitsuBig", line: "edo.mosuke.opt.okitsu.big", once: true, say: ["edo.mosuke.okitsu.big"] },
          bye("byeBig", "edo.mosuke.opt.bye.big", ["edo.mosuke.bye"]),
        ],
      },
      lil: {
        options: [
          { id: "lookLil", line: "edo.mosuke.opt.look.lil", once: true, say: ["edo.mosuke.look.lil"] },
          { id: "whyLil", line: "edo.mosuke.opt.why.lil", once: true, when: (g) => g.asked("mosuke/lookLil") > 0, say: ["edo.mosuke.why.lil"] },
          bye("byeLil", "edo.mosuke.opt.bye.lil", ["edo.mosuke.bye.lil"]),
        ],
      },
      shore: { say: ["edo.satta.name.1", "edo.satta.name.2", "edo.satta.name.3"], then: (g) => { g.flag("edo.oldShoreHeard", true); return "root"; } },
      pole: { say: ["edo.mosuke.pole"], then: async (g) => { await run(h, "pole", g); g.flag("edo.poleLent", true); return "exit"; } },
    },
  };
};

// ======================================================================================================
// THE SHIP (#26 Etekō, #27 Don't Lift The Lid): the deck, the fifth day out. WRITE-25 and PUZZLE-25 (round twenty-five,
// docs/WRITING.md): every line rewritten, and both puzzles rebuilt fair and richer (docs/PUZZLES-japan.md, #26 and #27).
//   #26  Kanbei cannot see his card for the noon sun. Big Sister reads it for him in the close-up (the lid tilted to shade
//        it: edo.cardShaded; the backwards card worked out: edo.compassRead), and calls the heading at once. Kanbei cannot see
//        which mark the needle is on, so the call is the first time the animal is named: "Monkey!", the word a ship never
//        hears (the deck freezes: edo.saruSaid). Kōta whispers the sailors' word to Little Sister, in charades or asked
//        (edo.seaWords), and she tells her sister; "Etekō!" (edo.headingCalled). The one who read the clock calls it, so Mom
//        and Little Sister, at Kanbei, are sent to Big Sister with whatever is still missing.
//   #27  Denzō says what is wrong: a quiet lady, an unhappy ship (the rice burnt, the boy homesick, nobody asking after her).
//        Mom's lesson with the lid (edo.lidDown); Little Sister's penny for Kōta's mother (edo.kotaMet, edo.coinTraded); the
//        lady's things, into Big Sister's note (edo.funadamaList). After each, the bosun listens at the mast; after the last,
//        Kōta laughs and she chirps (edo.chirped).
// ======================================================================================================
/** #27: is it done but for the chirp? The chirp follows the last of the four (Kōta met, the lid, the list, the coin). */
const chirpReady = (g) => is(g, "edo.kotaMet") && is(g, "edo.lidDown") && is(g, "edo.funadamaList") && is(g, "edo.coinTraded") && !is(g, "edo.chirped");
/** The chirp's nodes, for a tree whose last action may be the last of the four: `chirpIn` says the lead-in, the hook, CHIRP. */
const chirpNodes = (h, leadIn) => ({
  chirpIn: { say: [leadIn], then: async (g) => { await run(h, "chirp", g); return "chirped"; } },
  chirped: { say: CHIRP, then: (g) => { g.flag("edo.chirped", true); return "exit"; } },
});
/** #27, one of the four just done: the chirp if it was the last; else the narrator's word that the bosun is listening, and on. */
const afterOne = (fact, listen, next, chirp = "chirpIn") => async (g) => {
  g.flag(fact, true);
  if (chirpReady(g)) return chirp;
  await g.say(listen);
  return next;
};
/** A goodbye for each of the three, each shown only to her (a team's menu holds one way out). */
const byes = (base, sayMom, sayBig, sayLil) => [
  { ...bye(`${base}Mom`, `edo.${base}.opt.bye.mom`, [sayMom]), when: (g) => lead(g) === "mom" },
  { ...bye(`${base}Big`, `edo.${base}.opt.bye.big`, [sayBig]), when: (g) => lead(g) === "bigsis" },
  { ...bye(`${base}Lil`, `edo.${base}.opt.bye.lil`, [sayLil]), when: (g) => lead(g) === "lilsis" },
];

/** #26: "Monkey!", and the deck goes still (edo.saruSaid). */
export const FREEZE = ["edo.deck.freeze.1", "edo.deck.freeze.2", "edo.deck.freeze.3", "edo.deck.freeze.4", "edo.deck.freeze.5",
  "edo.deck.freeze.6", "edo.deck.freeze.7", "edo.deck.freeze.8", "edo.deck.freeze.9", "edo.deck.freeze.10", "edo.deck.freeze.11",
  "edo.deck.freeze.12"];
/** #26: Big Sister's first look at the needle in the shade: the working-out (edo.compassRead), ending on Kanbei's "Call it". */
export const WORKING = ["edo.compass.first.1", "edo.compass.first.2", "edo.compass.first.3", "edo.compass.first.4", "edo.compass.first.5",
  "edo.compass.first.6"];

/** kanbeiTree: Kanbei, the old helmsman, at the compass box (the ship's clock). He cannot see the card in the noon glare, and
    will not say so. The close-up is opened by his tree (`closeup`); the call is the tree's node `call`, Big Sister's (the one
    who read the clock calls it), begun straight after the reading (the close-up's needle, edo-compass.js, steps back to the
    deck and starts it there), or when she comes back to him. */
export const kanbeiTree = (h = {}) => {
  const read = (g) => is(g, "edo.compassRead");
  const stuck = (g) => is(g, "edo.saruSaid") && !is(g, "edo.seaWords");          // "Monkey!" said, and no other word for it yet
  return {
    id: "kanbei",
    start: (g) => {
      if (is(g, "edo.headingCalled")) return "after";
      if (!is(g, "edo.kanbeiMet")) return { mom: "openMom", big: "openBig", lil: "openLil" }[node(g)];
      if (read(g) && lead(g) === "bigsis") return stuck(g) ? "callWord" : "callAgain";
      return node(g);
    },
    nodes: {
      openBig: { say: ["edo.kanbei.big.1", "edo.kanbei.big.2", "edo.kanbei.big.3"], then: (g) => { g.flag("edo.kanbeiMet", true); return read(g) ? (stuck(g) ? "callWord" : "callAgain") : "big"; } },
      openMom: { say: ["edo.kanbei.mom.1", "edo.kanbei.mom.2"], then: (g) => { g.flag("edo.kanbeiMet", true); return "mom"; } },
      openLil: { say: ["edo.kanbei.lil.1", "edo.kanbei.lil.2", "edo.kanbei.lil.3"], then: (g) => { g.flag("edo.kanbeiMet", true); return "lil"; } },
      big: {
        options: [
          // the card, looked at: the close-up opens when the talk is over (the reading is the close-up's)
          { id: "lookBig", line: "edo.kanbei.opt.look.big", clue: true, when: (g) => !is(g, "edo.compassRead"), then: async (g) => { await run(h, "closeup", g); return "exit"; } },
          bye("byeBig", "edo.kanbei.opt.bye.big", ["edo.kanbei.bye"]),
        ],
      },
      // the call (Big Sister's): what is known decides what can be called (the monkey, until it is known that it is not said;
      // the sea word, once Little Sister has it from Kōta)
      callAgain: { say: ["edo.kanbei.call"], then: "call" },
      callWord: { say: ["edo.kanbei.call.again"], then: "call" },
      call: {
        options: [
          { id: "monkey", line: "edo.kanbei.call.opt.monkey", when: (g) => !is(g, "edo.saruSaid") && !is(g, "edo.seaWords"),
            then: async (g) => { await run(h, "freeze", g); return "freeze"; } },
          { id: "eteko", line: "edo.kanbei.call.opt.eteko", when: (g) => is(g, "edo.seaWords"), then: "called" },
          { id: "what", line: "edo.kanbei.call.opt.what", clue: true, when: stuck, say: ["edo.kanbei.call.what"] },
          { id: "wait", line: "edo.kanbei.call.opt.wait", say: ["edo.kanbei.call.wait"], then: "exit" },
        ],
      },
      freeze: { say: FREEZE, then: (g) => { g.flag("edo.saruSaid", true); return "exit"; } },
      called: { say: ["edo.deck.call.1", "edo.deck.call.2"], then: async (g) => { await run(h, "hold", g); return "held"; } },
      held: { say: ["edo.deck.call.3", "edo.deck.call.4", "edo.deck.call.5"], then: (g) => { g.flag("edo.headingCalled", true); return "exit"; } },
      // Mom and Little Sister offer to call it; he sends them to Big Sister, with whatever is still missing
      mom: {
        options: [
          { id: "eyesMom", line: "edo.kanbei.opt.eyes.mom", once: true, say: ["edo.kanbei.eyes.mom"] },
          ...callFor("Mom", "edo.kanbei.opt.call.mom", "edo.kanbei.call.mom"),
          bye("byeMom", "edo.kanbei.opt.bye.mom", ["edo.kanbei.bye"]),
        ],
      },
      lil: {
        options: [
          { id: "clockLil", line: "edo.kanbei.opt.clock.lil", once: true, say: ["edo.kanbei.clock.lil"] },
          ...callFor("Lil", "edo.kanbei.opt.call.lil", "edo.kanbei.call.lil"),
          bye("byeLil", "edo.kanbei.opt.bye.lil", ["edo.kanbei.bye"]),
        ],
      },
      after: { say: ["edo.kanbei.after"], options: byes("kanbei", "edo.kanbei.bye", "edo.kanbei.bye", "edo.kanbei.bye").map((o) => ({ ...o, id: `after${o.id}` })) },
    },
  };
  /** Mom's or Little Sister's offer to call the heading, once the clock is read: one answer for each state of #26 (before
      the word that is not said; after it; the sailors' word found), each once. */
  function callFor(who, line, base) {
    return [
      { id: `call${who}`, line, once: true, when: (g) => read(g) && !is(g, "edo.saruSaid") && !is(g, "edo.seaWords"), say: [base] },
      { id: `call${who}Word`, line, once: true, when: stuck, say: [`${base}.word`] },
      { id: `call${who}Ready`, line, once: true, when: (g) => read(g) && is(g, "edo.seaWords"), say: [`${base}.ready`] },
    ];
  }
};

/** denzoTree: Denzō, the bosun. The first time, the goal of #27: she has not chirped; a happy ship is a happy lady, and this
    one is not (the rice, the boy, nobody asking after her). What she was given (the list, into Big Sister's note); the cask
    for Konpira; and, once the word has been said that is not said at sea, he will not say what is said instead. */
const OPEN_DENZO = ["edo.denzo.open.1", "edo.denzo.open.2", "edo.denzo.open.3", "edo.denzo.open.4"];
export const denzoTree = (h = {}) => {
  const list = (id, line) => ({ id, line, clue: true, when: (g) => !is(g, "edo.funadamaList"), then: "list" });
  const notNow = (id, line, say) => ({ id, line, clue: true, when: (g) => is(g, "edo.saruSaid") && !is(g, "edo.seaWords"), say: [say] });
  return {
    id: "denzo",
    start: (g) => (is(g, "edo.chirped") ? "after" : is(g, "edo.denzoMet") ? node(g) : "first"),
    nodes: {
      first: { say: OPEN_DENZO, then: (g) => { g.flag("edo.denzoMet", true); return node(g); } },
      // the first knock on the mast step, or Big Sister's note held out, before he has said what is wrong: that, then her list
      firstList: { say: OPEN_DENZO, then: (g) => { g.flag("edo.denzoMet", true); return "list"; } },
      mom: {
        options: [
          { id: "worryMom", line: "edo.denzo.opt.worry.mom", once: true, say: ["edo.denzo.worry.1", "edo.denzo.worry.2"] },
          list("listMom", "edo.denzo.opt.list.mom"),
          notNow("notNowMom", "edo.denzo.opt.notnow.mom", "edo.denzo.notnow.mom"),
          bye("byeMom", "edo.denzo.opt.bye.mom", ["edo.denzo.bye"]),
        ],
      },
      // TALK-24: Big Sister's questions about the lady and the cask in the sea are a topic of their own
      big: {
        options: [
          list("listBig", "edo.denzo.opt.list.big"),
          notNow("notNowBig", "edo.denzo.opt.notnow.big", "edo.denzo.notnow.big"),
          topic("loreBig", "edo.denzo.topic.lore.big", "loreBig"),
          bye("byeBig", "edo.denzo.opt.bye.big", ["edo.denzo.bye"]),
        ],
      },
      loreBig: {
        options: [
          { id: "worryBig", line: "edo.denzo.opt.worry.big", once: true, say: ["edo.denzo.worry.1", "edo.denzo.worry.2"] },
          { id: "chirpBig", line: "edo.denzo.opt.chirp.big", once: true, say: ["edo.denzo.chirp.big"] },
          { id: "caskBig", line: "edo.denzo.opt.cask.big", once: true, say: ["edo.denzo.cask.big"] },
          back("loreBig"),
        ],
      },
      lil: {
        options: [
          list("listLil", "edo.denzo.opt.list.lil"),
          notNow("notNowLil", "edo.denzo.opt.notnow.lil", "edo.denzo.notnow.lil"),
          { id: "patLil", line: "edo.denzo.opt.pat.lil", once: true, say: ["edo.denzo.pat.lil"] },
          bye("byeLil", "edo.denzo.opt.bye.lil", ["edo.denzo.bye.lil"]),
        ],
      },
      // what the lady was given; Big Sister writes it in her note (edo.funadamaList)
      list: { say: LIST, then: async (g) => { await run(h, "write", g); return afterOne("edo.funadamaList", "edo.deck.listen.list", "root")(g); } },
      ...chirpNodes(h, "edo.deck.chirp.list"),
      after: { say: ["edo.denzo.after"], options: byes("denzo", "edo.denzo.bye", "edo.denzo.bye", "edo.denzo.bye.lil").map((o) => ({ ...o, id: `after${o.id}` })) },
    },
  };
};

/** seijiroTree: Seijirō, the purser. Cargo, then passengers (the crew fed), then crew (the lady chirped). */
export const seijiroTree = (h = {}) => ({
  id: "seijiro",
  start: "open",
  nodes: {
    open: {
      say: ["edo.seijiro.open"],
      options: [
        { id: "whatBig", line: "edo.seijiro.opt.what.big", keep: true,
          then: (g) => (is(g, "edo.chirped") ? "crew" : is(g, "edo.lidDown") ? "passengers" : "cargo") },
        { id: "cargoMom", line: "edo.seijiro.opt.cargo.mom", once: true, say: ["edo.seijiro.cargo.mom"] },
        { id: "countLil", line: "edo.seijiro.opt.count.lil", once: true, say: ["edo.seijiro.count.lil.1", "edo.seijiro.count.lil.2", "edo.seijiro.count.lil.3"] },
        ...byes("seijiro", "edo.seijiro.bye", "edo.seijiro.bye", "edo.seijiro.bye"),
      ],
    },
    cargo: { say: ["edo.seijiro.what.1"], then: "exit" },
    passengers: { say: ["edo.seijiro.what.2"], then: "exit" },
    crew: { say: ["edo.seijiro.what.3"], then: "exit" },
  },
});

/** kotaTree: Kōta, the cook, twelve, on his first voyage. Little Sister's guessing game (the Grump; a cat, a word a ship never
    hears; a monkey, and the sailors' word for it, etekō); his mother in Yui, and something from far away for her (the penny,
    for his coin); Mom's lesson with the lid; and the chirp, if his was the last of the four. Shy of Big Sister. */
export const kotaTree = (h = {}) => ({
  id: "kota",
  start: (g) => (is(g, "edo.chirped") ? "after" : is(g, "edo.kotaMet") ? node(g) : { mom: "openMom", big: "openBig", lil: "openLil" }[node(g)]),
  nodes: {
    openLil: { say: ["edo.kota.open.lil.1", "edo.kota.open.lil.2", "edo.kota.open.lil.3"], then: (g) => { g.flag("edo.kotaMet", true); return "lil"; } },
    openMom: { say: ["edo.kota.open.mom"], then: (g) => { g.flag("edo.kotaMet", true); return "mom"; } },
    openBig: { say: ["edo.kota.open.big", "edo.kota.open.big.2"], then: (g) => { g.flag("edo.kotaMet", true); return "big"; } },
    lil: {
      options: [
        { id: "gameLil", line: "edo.kota.opt.game.lil", keep: true,
          when: (g) => !(g.asked("kota/grump") && g.asked("kota/cat") && g.asked("kota/monkey")), say: ["edo.kota.game"], then: "game" },
        { id: "homeLil", line: "edo.kota.opt.home.lil", once: true, say: ["edo.kota.home.1", "edo.kota.home.2", "edo.kota.home.3", "edo.kota.home.4", "edo.kota.home.5"] },
        // after the word was said on deck: he whispers the sailors' one to her (or she had it in the game: edo.seaWords)
        { id: "wordLil", line: "edo.kota.opt.word.lil", clue: true, when: (g) => is(g, "edo.saruSaid") && !is(g, "edo.seaWords"),
          say: ["edo.kota.word.lil.1", "edo.kota.word.lil.2", "edo.kota.word.lil.3"], set: "edo.seaWords" },
        { id: "penniesLil", line: "edo.kota.opt.pennies.lil", clue: true, when: (g) => g.has("pennies") && !is(g, "edo.coinTraded"), then: "coin" },
        bye("byeLil", "edo.kota.opt.bye.lil", ["edo.kota.bye.lil"]),
      ],
    },
    // the guessing game: she acts, he guesses
    game: {
      options: [
        { id: "grump", line: "edo.kota.opt.grump.lil", once: true, say: ["edo.kota.grump.0", "edo.kota.grump.1", "edo.kota.grump.2", "edo.kota.grump.3", "edo.kota.grump.4"] },
        { id: "cat", line: "edo.kota.opt.cat.lil", once: true, say: ["edo.kota.cat.0", "edo.kota.cat.1", "edo.kota.cat.2", "edo.kota.cat.3"] },
        { id: "monkey", line: "edo.kota.opt.monkey.lil", once: true, then: (g) => (is(g, "edo.saruSaid") ? "monkeyAfter" : "monkeyFirst") },
        { id: "stop", line: "edo.kota.opt.stop.lil", then: "lil" },
      ],
    },
    monkeyFirst: { say: ["edo.kota.monkey.0", "edo.kota.monkey.1", "edo.kota.monkey.2", "edo.kota.monkey.3"], then: (g) => { g.flag("edo.seaWords", true); return "back"; } },
    monkeyAfter: { say: ["edo.kota.monkey.0", "edo.kota.monkey.after", "edo.kota.monkey.3"], then: (g) => { g.flag("edo.seaWords", true); return "back"; } },
    // the penny for a coin (for his mother, who has never seen anything from so far away)
    coin: { say: ["edo.deck.coin.1", "edo.deck.coin.2", "edo.deck.coin.3"], then: async (g) => { await run(h, "look", g); return "trade"; } },
    trade: { say: ["edo.deck.coin.4", "edo.deck.coin.4b"], then: async (g) => { await run(h, "trade", g); return "traded"; } },
    traded: { say: ["edo.deck.coin.5", "edo.deck.coin.mom", "edo.deck.coin.bigsis"], then: afterOne("edo.coinTraded", "edo.deck.listen.coin", "lil", "chirpCoin") },
    chirpCoin: { say: ["edo.deck.chirp.coin"], then: async (g) => { await run(h, "chirp", g); return "chirped"; } },
    mom: {
      options: [
        { id: "lidMom", line: "edo.kota.opt.lid.mom", clue: true, when: (g) => !is(g, "edo.lidDown"), then: "lid" },
        { id: "homeMom", line: "edo.kota.opt.home.mom", once: true, say: ["edo.kota.home.mom"] },
        bye("byeMom", "edo.kota.opt.bye.mom", ["edo.kota.bye.mom"]),
      ],
    },
    // Mom's lesson: don't lift the lid; the waiting; the crew eat (edo.lidDown)
    lid: { say: ["edo.deck.lid.1", "edo.deck.lid.2", "edo.deck.lid.3", "edo.deck.lid.4"], then: async (g) => { await run(h, "wait", g); return "waiting"; } },
    waiting: { say: ["edo.deck.wait.1", "edo.deck.wait.2", "edo.deck.wait.3", "edo.deck.wait.4", "edo.deck.wait.5", "edo.deck.wait.6", "edo.deck.wait.7", "edo.deck.wait.8"],
      then: async (g) => { await run(h, "serve", g); return "eaten"; } },
    eaten: { say: ["edo.deck.eat.1", "edo.deck.eat.2", "edo.deck.eat.3", "edo.deck.eat.4"], then: afterOne("edo.lidDown", "edo.deck.listen.lid", "mom", "chirpLid") },
    chirpLid: { say: ["edo.deck.chirp.lid"], then: async (g) => { await run(h, "chirp", g); return "chirped"; } },
    chirped: { say: CHIRP, then: (g) => { g.flag("edo.chirped", true); return "exit"; } },
    big: {
      options: [
        { id: "lidBig", line: "edo.kota.opt.lid.big", once: true, when: (g) => !is(g, "edo.lidDown"), say: ["edo.kota.lid.big", "edo.kota.lid.big.2"] },
        { id: "wordBig", line: "edo.kota.opt.word.big", clue: true, when: (g) => is(g, "edo.saruSaid") && !is(g, "edo.seaWords"), say: ["edo.kota.word.big", "edo.kota.word.big.2"] },
        bye("byeBig", "edo.kota.opt.bye.big", ["edo.kota.bye.big"]),
      ],
    },
    after: { say: ["edo.kota.after"], options: byes("kota", "edo.kota.bye.mom", "edo.kota.bye.big", "edo.kota.bye.lil").map((o) => ({ ...o, id: `after${o.id}` })) },
  },
});

/** gonrokuDeckTree: Gonroku, at the tiller, on the fifth day. He talks about the weather. Once the heading is called he says so
    first, and the rest is as before (the voyage, his thanks, the one goodbye). */
export const gonrokuDeckTree = (h = {}) => ({
  id: "gonrokuDeck",
  start: (g) => (is(g, "edo.headingCalled") ? "late" : "open"),
  nodes: {
    open: { say: ["edo.deck.gonroku.open"], then: "menu" },
    late: { say: ["edo.deck.gonroku.after"], then: "menu" },
    menu: {
      // TALK-24: the sea, the days to Osaka and the steering are a topic (the voyage); one goodbye, the one being played's
      options: [
        { id: "clockBig", line: "edo.deck.gonroku.opt.clock.big", clue: true, when: (g) => !is(g, "edo.compassRead"), say: ["edo.deck.gonroku.clock.big"] },
        topic("voyage", "edo.deck.gonroku.topic.voyage", "voyage"),
        { id: "thanksMom", line: "edo.deck.gonroku.opt.thanks.mom", once: true, when: (g) => !is(g, "edo.lidDown"), say: ["edo.deck.gonroku.thanks.1"] },
        { id: "thanksRiceMom", line: "edo.deck.gonroku.opt.thanks.mom", once: true, when: (g) => is(g, "edo.lidDown"), say: ["edo.deck.gonroku.thanks.2"] },
        ...byes("deck.gonroku", "edo.deck.gonroku.bye.mom", "edo.deck.gonroku.bye.big", "edo.deck.gonroku.bye.lil").map((o, i) => ({ ...o, id: ["byeMom", "byeBig", "byeLil"][i] })),
      ],
    },
    voyage: {
      options: [
        { id: "seaMom", line: "edo.deck.gonroku.opt.sea.mom", once: true, say: ["edo.deck.gonroku.sea.1", "edo.deck.gonroku.sea.2", "edo.deck.gonroku.sea.3"] },
        { id: "osakaBig", line: "edo.deck.gonroku.opt.osaka.big", once: true, say: ["edo.deck.gonroku.osaka.big"] },
        { id: "steerLil", line: "edo.deck.gonroku.opt.steer.lil", once: true, say: ["edo.deck.gonroku.steer.1", "edo.deck.gonroku.steer.2", "edo.deck.gonroku.steer.3"] },
        back("voyage"),
      ],
    },
  },
});

// ======================================================================================================
// OSAKA (#28 The Dōjima Shore, #29 What The Road God Said, #30 Berlin Blue, #31 Three To A Puppet)
// ======================================================================================================
/** natsuTree: O-Natsu at her alms stall. Mom asks to help, and is handed the paddle (edo.paddle); the tasks are the scene's
    (the pot, the tray, the tub; FIFTH; VOUCH); then their own supper on the steps (edo.supped). */
export const natsuTree = (h = {}) => ({
  id: "natsu",
  start: (g) => {
    if (is(g, "edo.supped")) return "after";
    if (is(g, "edo.vouched")) return "supper";
    if (!is(g, "edo.natsuMet")) return "first";
    if (is(g, "edo.paddle")) return "busy";
    return node(g);
  },
  nodes: {
    first: { say: ["edo.natsu.open"], then: (g) => { g.flag("edo.natsuMet", true); return node(g); } },
    mom: {
      options: [
        { id: "helpMom", line: "edo.natsu.opt.help.mom", clue: true, when: (g) => !is(g, "edo.paddle"), then: "paddle" },
        { id: "whyMom", line: "edo.natsu.opt.why.mom", once: true, say: ["edo.natsu.why.mom"] },
        bye("byeMom", "edo.natsu.opt.bye.mom", ["edo.natsu.bye"]),
      ],
    },
    big: {
      options: [
        { id: "aloneBig", line: "edo.natsu.opt.alone.big", once: true, say: ["edo.natsu.alone.1", "edo.natsu.alone.2"] },
        { id: "husbandBig", line: "edo.natsu.opt.husband.big", once: true, when: (g) => g.asked("natsu/aloneBig") > 0, say: ["edo.natsu.husband.big"] },
        bye("byeBig", "edo.natsu.opt.bye.big", ["edo.natsu.bye"]),
      ],
    },
    lil: {
      options: [
        { id: "foodLil", line: "edo.natsu.opt.food.lil", once: true, say: ["edo.natsu.food.lil"] },
        { id: "boyLil", line: "edo.natsu.opt.boy.lil", once: true, say: ["edo.natsu.boy.lil"] },
        bye("byeLil", "edo.natsu.opt.bye.lil", ["edo.natsu.bye"]),
      ],
    },
    // she looks at Mom a moment, and hands her the paddle: the pot is hers; then the three tasks, named
    paddle: { say: ["edo.natsu.paddle.1", "edo.natsu.paddle.2"], then: async (g) => { await run(h, "paddle", g); return "tasks"; } },
    tasks: { say: ["edo.natsu.paddle.3", "edo.natsu.paddle.4"], then: (g) => { g.flag("edo.paddle", true); return "exit"; } },
    busy: { say: ["edo.natsu.busy"], then: "exit" },
    // their own supper, on the steps
    supper: { say: ["edo.dojima.supper.1"], then: async (g) => { await run(h, "sit", g); return "grace"; } },
    grace: { say: ["edo.dojima.supper.2", "edo.dojima.supper.3"], then: async (g) => { await run(h, "eat", g); return "fed"; } },
    fed: { say: ["edo.dojima.supper.4", "edo.dojima.supper.5", "edo.dojima.supper.6", "edo.dojima.supper.7", "edo.dojima.supper.8"],
      then: async (g) => { await run(h, "giveBack", g); g.flag("edo.supped", true); return "exit"; } },
    after: { say: ["edo.natsu.after"], then: "exit" },
  },
});

/** riheiTree: Rihei, her husband, wet. */
export const riheiTree = (h = {}) => ({
  id: "rihei",
  start: "open",
  nodes: {
    open: {
      say: ["edo.rihei.open"],
      options: [
        { id: "whoMom", line: "edo.rihei.opt.who.mom", once: true, say: ["edo.rihei.who.mom"] },
        { id: "whyBig", line: "edo.rihei.opt.why.big", once: true, say: ["edo.rihei.why.big"] },
        { id: "moneyBig", line: "edo.rihei.opt.money.big", once: true, when: (g) => g.asked("rihei/whyBig") > 0, say: ["edo.rihei.money.big"] },
        { id: "splashLil", line: "edo.rihei.opt.splash.lil", once: true, say: ["edo.rihei.splash.lil"] },
        bye("byeMom", "edo.rihei.opt.bye.mom", ["edo.rihei.bye"]),
      ],
    },
  },
});

/** kyuhachiTree: Kyūhachi, who lives on alms. His ladle, for a share: "Nobody ever says yes." */
export const kyuhachiTree = (h = {}) => ({
  id: "kyuhachi",
  start: (g) => (is(g, "edo.paddle") ? "after" : "open"),
  nodes: {
    open: {
      say: ["edo.kyuhachi.open"],
      options: [
        { id: "timesMom", line: "edo.kyuhachi.opt.times.mom", once: true, say: ["edo.kyuhachi.times.mom"], then: "offer" },
        { id: "whereBig", line: "edo.kyuhachi.opt.where.big", once: true, say: ["edo.kyuhachi.where.big"] },
        { id: "countLil", line: "edo.kyuhachi.opt.count.lil", once: true, say: ["edo.kyuhachi.count.lil"] },
        bye("byeLil", "edo.kyuhachi.opt.bye.lil", ["edo.kyuhachi.bye.lil"]),
      ],
    },
    // the wrong try: his ladle, lent for a share
    offer: { say: ["edo.kyuhachi.offer.1", "edo.kyuhachi.offer.2", "edo.kyuhachi.offer.3"], then: "open" },
    after: { say: ["edo.kyuhachi.after"], then: "exit" },
  },
});

/** natsuStreetTree: O-Natsu at the crossroads. The custom (the boxwood comb); Mom's prayer (Jeremiah 31:17); the first words
    (the yomiuri); the chant (edo.heardShosha); the magistrate's men and the sheet (edo.sheetCaught, edo.followed); the comb
    and the slip, given (edo.combGiven). */
export const natsuStreetTree = (h = {}) => ({
  id: "natsuStreet",
  start: (g) => (is(g, "edo.combGiven") ? "after" : "open"),
  nodes: {
    open: {
      say: ["edo.natsu.street.open"],
      options: [
        { id: "readyMom", line: "edo.natsu.street.opt.ready.mom", then: "custom" },
        { id: "readyBig", line: "edo.natsu.street.opt.ready.big", then: "custom" },
        { id: "readyLil", line: "edo.natsu.street.opt.ready.lil", say: ["edo.natsu.street.lil"], then: "custom" },
      ],
    },
    custom: { say: ["edo.street.comb.1", "edo.street.comb.2", "edo.street.comb.3", "edo.street.comb.4", "edo.street.comb.5", "edo.street.comb.6"],
      then: async (g) => { await run(h, "pray", g); return "prayer"; } },
    prayer: { say: ["edo.street.pray.1", "edo.street.pray.2", "edo.street.pray.3"],
      then: async (g) => { g.flag("edo.combAsked", true); await run(h, "sellers", g); return "first"; } },
    first: { say: ["edo.street.first.1", "edo.street.first.2", "edo.street.first.3", "edo.street.first.4"], then: "chant" },
    chant: { say: ["edo.street.chant.1", "edo.street.chant.2", "edo.street.chant.3", "edo.street.chant.4", "edo.street.chant.5", "edo.street.chant.6",
      "edo.street.heard.1", "edo.street.heard.2", "edo.street.heard.3"],
      then: async (g) => { g.flag("edo.heardShosha", true); await run(h, "men", g); return "men"; } },
    men: { say: ["edo.street.men.1", "edo.street.men.2", "edo.street.men.3", "edo.street.men.4", "edo.street.men.5", "edo.street.men.6"],
      then: async (g) => { g.flag("edo.sheetCaught", true); g.flag("edo.followed", true); await run(h, "gift", g); return "gift"; } },
    gift: { say: ["edo.street.gift.1", "edo.street.gift.2", "edo.street.gift.3", "edo.street.gift.4"],
      then: (g) => { g.flag("edo.combGiven", true); return "exit"; } },
    after: {
      say: ["edo.natsu.street.after"],
      options: [
        { id: "thanksMom", line: "edo.natsu.street.opt.thanks.mom", once: true, say: ["edo.natsu.street.thanks.mom"] },
        bye("byeLil", "edo.natsu.street.opt.bye.lil", ["edo.natsu.street.bye.lil"]),
        bye("byeBig", "edo.natsu.street.opt.bye.big", ["edo.natsu.street.bye.big"]),
      ],
    },
  },
});

/** senzoTree: Senzō, the printer. The marks, watched (edo.marksSeen); the laying is the scene's (LAY); the sheet, read
    aloud (edo.sheetRead) once the paper has been laid in order (edo.registered). */
export const senzoTree = (h = {}) => {
  const sheet = (id, line) => ({ id, line, when: (g) => is(g, "edo.registered") && is(g, "edo.sheetCaught") && !is(g, "edo.sheetRead"), then: "sheet" });
  return {
    id: "senzo",
    start: (g) => (!is(g, "edo.senzoMet") ? "first" : is(g, "edo.sheetRead") ? "later" : node(g)),
    nodes: {
      first: { say: ["edo.senzo.open"], then: (g) => { g.flag("edo.senzoMet", true); return node(g); } },
      later: { say: ["edo.senzo.after"], then: node },
      big: {
        options: [
          { id: "watchBig", line: "edo.senzo.opt.watch.big", clue: true, when: (g) => !is(g, "edo.marksSeen"), say: ["edo.senzo.watch"], then: "watch" },
          { id: "actorsBig", line: "edo.senzo.opt.actors.big", once: true, say: ["edo.senzo.actors.big"] },
          sheet("sheetBig", "edo.senzo.sheet.opt.big"),
          bye("byeBig", "edo.senzo.opt.bye.big", ["edo.senzo.bye"]),
        ],
      },
      mom: {
        options: [
          { id: "leftMom", line: "edo.senzo.opt.left.mom", once: true, say: ["edo.senzo.left.mom"] },
          sheet("sheetMom", "edo.senzo.sheet.opt.mom"),
          bye("byeMom", "edo.senzo.opt.bye.mom", ["edo.senzo.bye"]),
        ],
      },
      lil: {
        options: [
          { id: "pictureLil", line: "edo.senzo.opt.picture.lil", once: true, say: ["edo.senzo.picture.lil.1", "edo.senzo.picture.lil.2", "edo.senzo.picture.lil.3"] },
          { id: "hallLil", line: "edo.senzo.opt.hall.lil", once: true, when: (g) => is(g, "edo.sheetRead"), say: ["edo.senzo.hall.lil"] },
          bye("byeLil", "edo.senzo.opt.bye.lil", ["edo.senzo.bye"]),
        ],
      },
      watch: { then: async (g) => { await run(h, "watch", g); return "marks"; } },
      marks: { say: ["edo.senzo.marks.1", "edo.senzo.marks.2", "edo.senzo.marks.3", "edo.senzo.marks.4", "edo.senzo.marks.5"],
        then: (g) => { g.flag("edo.marksSeen", true); return "exit"; } },
      sheet: { say: ["edo.senzo.sheet.1", "edo.senzo.sheet.2"], then: async (g) => { await run(h, "curtain", g); return "read"; } },
      read: { say: ["edo.sheet.1", "edo.sheet.2", "edo.sheet.3", "edo.sheet.4", "edo.sheet.5", "edo.sheet.6", "edo.sheet.7",
        "edo.sheet.after.1", "edo.sheet.after.2", "edo.sheet.after.3"], then: (g) => { g.flag("edo.sheetRead", true); return "exit"; } },
    },
  };
};
/** Sōshichi's print shown to Senzō (the toyamaprint used on him, by whoever carries it). */
export const SENZO_TOYAMA = ["edo.senzo.toyama.1", "edo.senzo.toyama.2", "edo.senzo.toyama.3"];

/** jubeiTree: Jūbei, the chief puppeteer. The rule of the black robes; the girls taken on (edo.hooded); one rule each,
    tried once (edo.rehearsed); after the show, who they are: the truth, and the road round Osaka (edo.troupeTaken). The
    seat and the show are the scene's (SEAT, SHOW). */
export const jubeiTree = (h = {}) => {
  const robes = (id, line) => ({ id, line, clue: true, when: (g) => !is(g, "edo.ruleHeard"), then: "rule" });
  const offer = (id, line) => ({ id, line, when: (g) => is(g, "edo.ruleHeard") && !is(g, "edo.hooded"), then: "choose" });
  const both = (g) => { if (is(g, "edo.rehearsedLeft") && is(g, "edo.rehearsedFeet")) g.flag("edo.rehearsed", true); };
  return {
    id: "jubei",
    start: (g) => (is(g, "edo.troupeTaken") ? "done" : is(g, "edo.cue3") ? "after" : is(g, "edo.jubeiMet") ? node(g) : "first"),
    nodes: {
      first: { say: ["edo.jubei.open.1", "edo.jubei.open.2", "edo.jubei.open.3"], then: (g) => { g.flag("edo.jubeiMet", true); return node(g); } },
      mom: {
        options: [
          { id: "whoMom", line: "edo.jubei.opt.who.mom", once: true, say: ["edo.jubei.who.mom"] },
          { id: "partMom", line: "edo.jubei.opt.part.mom", once: true, when: (g) => is(g, "edo.hooded"), say: ["edo.jubei.wrong.mom"] },
          bye("byeMom", "edo.jubei.opt.bye.mom", ["edo.jubei.bye"]),
        ],
      },
      big: {
        options: [
          robes("robesBig", "edo.jubei.opt.robes.big"),
          offer("offerBig", "edo.jubei.opt.offer.big"),
          { id: "leftBig", line: "edo.jubei.opt.left.big", clue: true, when: (g) => is(g, "edo.hooded") && !is(g, "edo.rehearsedLeft"), then: "left" },
          { id: "feetBig", line: "edo.jubei.opt.feet.big", once: true, when: (g) => is(g, "edo.hooded"), say: ["edo.jubei.wrong.big"] },
          bye("byeBig", "edo.jubei.opt.bye.big", ["edo.jubei.bye"]),
        ],
      },
      lil: {
        options: [
          robes("robesLil", "edo.jubei.opt.robes.lil"),
          offer("offerLil", "edo.jubei.opt.offer.lil"),
          { id: "feetLil", line: "edo.jubei.opt.feet.lil", clue: true, when: (g) => is(g, "edo.hooded") && !is(g, "edo.rehearsedFeet"), then: "feet" },
          { id: "handLil", line: "edo.jubei.opt.hand.lil", once: true, when: (g) => is(g, "edo.hooded"), say: ["edo.jubei.wrong.lil"] },
          bye("byeLil", "edo.jubei.opt.bye.lil", ["edo.jubei.bye.lil"]),
        ],
      },
      // the black robes: the house agrees not to see them
      rule: { say: ["edo.jubei.rule.1", "edo.jubei.rule.2", "edo.jubei.rule.3"], then: (g) => { g.flag("edo.ruleHeard", true); return "root"; } },
      // he looks at them, at the time, at the robes
      choose: { say: ["edo.jubei.choose.1", "edo.jubei.choose.2"], then: async (g) => { await run(h, "robes", g); return "hooded"; } },
      hooded: { say: ["edo.jubei.three"], then: (g) => { g.flag("edo.hooded", true); return "root"; } },
      // one rule each, tried once on the stand
      left: { say: ["edo.jubei.left.1"], then: async (g) => { await run(h, "practise", g); return "leftDone"; } },
      leftDone: { say: ["edo.jubei.left.2", "edo.jubei.left.3"], then: (g) => { g.flag("edo.rehearsedLeft", true); both(g); return "root"; } },
      feet: { say: ["edo.jubei.feet.1"], then: async (g) => { await run(h, "practise", g); return "feetDone"; } },
      feetDone: { say: ["edo.jubei.feet.2", "edo.jubei.feet.3"], then: (g) => { g.flag("edo.rehearsedFeet", true); both(g); return "root"; } },
      // after the show: who are you? The truth (Mom's), and the road round Osaka
      after: {
        say: ["edo.jubei.after.1"],
        options: [
          { id: "truthMom", line: "edo.jubei.opt.truth.mom", then: "road" },
          { id: "againLil", line: "edo.jubei.opt.again.lil", once: true, say: ["edo.jubei.again.lil"] },
          { id: "learnBig", line: "edo.jubei.opt.learn.big", once: true, say: ["edo.jubei.learn.big"] },
        ],
      },
      road: { say: ["edo.jubei.road.1", "edo.jubei.road.2", "edo.jubei.road.3", "edo.jubei.road.4", "edo.jubei.road.4b", "edo.jubei.road.5"],
        then: (g) => { g.flag("edo.troupeTaken", true); return "exit"; } },
      done: { say: ["edo.jubei.bye"], then: "exit" },
    },
  };
};

/** Every tree, by name, for the tests. */
export const trees = { kuniTree, bearersTree, soshichiTree, shigeTree, mosukeTree, kanbeiTree, denzoTree, seijiroTree, kotaTree,
  gonrokuDeckTree, natsuTree, riheiTree, kyuhachiTree, natsuStreetTree, senzoTree, jubeiTree };

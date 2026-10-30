// The talks of Act Six's first leg: Yui on Suruga Bay (WRITE-20A: new in round twenty; briefs/WRITE-20.md, and the design,
// briefs/out/edo-design.md, section 7, #21 to #24). Plain data in the engine's format (docs/DESIGN.md, section 7,
// "Dialogue trees"), made as js/content/talk/nevada.js and talk/office.js make them: every word is a line id
// (js/content/lines/edo-a.en.js). An option's `line` is said by the one it belongs to (Mom, Big Sister or Little Sister:
// the three are a team, all on stage, so a menu may mix their lines, as the letterbox's did); its `say` is the reply (a
// list, or { 1, 2, more } by how many times it has been picked); `set` makes facts true; `do` is a script; `then` goes to
// a node, "back", "root" or "exit" (or is a function of the game giving one). TALK-18's rule holds: a picked option is
// gone unless it is a clue (`clue: true`), a way out, or a topic. MERGE-20 joins this file with WRITE-20B's talk/edo-b.js.
//
// Each tree is a function of a `hooks` object, so that the scene hands in the scripts a branch needs:
//     import { kiheiTree } from "../talk/edo-a.js";
//     const KIHEI = kiheiTree({ press, serve, bow, under, giveBox });
//     ...  use: (g) => g.talk(KIHEI)
// A hook that is not handed in is passed over (the talk still says every line and sets every fact).
//
// THE HOOKS, and what each must do. None of them says a line the tree says; the one that says lines (dress) says only those.
//   tamiTree (O-Tami, at her place in the shop, the baby on her back or in its basket; #22)
//     lullaby(g)    Mom takes the baby and rocks her, and hums: a tune with no words (the game's own; a stage direction,
//                   never a line), until the baby sleeps in the middle of O-Tami's sentence (the tree says the sentence,
//                   edo.shop.baby.3, before it, and O-Tami's "What did you DO." after). The baby stays asleep in its basket
//                   from here on (the cut-out's second state; tami without the baby on her back). Staging and music. (The
//                   tree sets edo.babySleeps after it.)
//     dress(g)      the kimonos: O-Tami goes to the chest, and SAYS edo.shop.dress.1 to .13 in order, swapping each lead's
//                   outfit to `edo` as her lines name it (Mom after .2, Big Sister after .4, Little Sister after .11, who
//                   keeps her boots; the hats after .6; sandals for Mom and Big Sister at .7: g.dress(who, "edo")). The
//                   tree says nothing of these itself. (The tree sets edo.clothes after it.)
//   kiheiTree (Kihei at his cutting board; #23)
//     press(g)      he presses the sushi, and the player watches: the rice into the box, the fish, the lid, his weight on
//                   it, the cut. Staging; the tree says Big Sister's watching aloud after it.
//     serve(g)      he sets the cut pieces on the step of the raised room; the three sit on the step (the cut-out `food`
//                   on the step from here until the meal's end). Staging.
//     bow(g)        after Little Sister's grace: Kihei and O-Tami wait, puzzled and polite, and then bow to the god-shelf,
//                   and say nothing. Staging (figure poses), no lines.
//     under(g)      the cat takes a mackerel off the board and goes under the raised floor (the cat's cut-out gone from her
//                   place: edo.shop.cat2.* are the looks after); Little Sister goes under after her (the `under` mark) and
//                   comes back with the fish, and a cobweb. (The tree sets edo.catGone after it.)
//     giveBox(g)    O-Tami wraps the rest for the road: g.give("sushibox") to whoever is playing; the `food` cut-out goes.
//                   (The tree sets edo.fed and edo.boxGiven after it.)
//   sankichiTree (Sankichi beside the board; #22's plant, and #21's "Bunsei thirteen")
//     boardOpen(g)  the close-up of the Kirishitan board (a picture: dense columns, a little roof), under which he reads.
//     boardClose(g) the close-up away, after his reading and the family's answer. (The tree sets edo.boardRead between.)
//   tokuzoTree (Tokuzō in the street, met dressed; #22's end)
//     home(g)       he has written "travellers, three, going west": he goes off along the street (the `east` end) and home,
//                   pleased, and is not on his rounds again unless the scene wants him (the `after` node serves if he is).
//                   (The tree sets edo.dressed before it: the beat of #22.)
//   gonrokuTree (Gonroku on the beach by his boat; #24): no hooks: every argument fails, and nothing moves.
//   masaTree (O-Masa at the net racks; #24's lever)
//     toGonroku(g)  she puts the net down and goes down the beach to her husband; the three stay where they are (she said
//                   so). What she says to him the player hears only the end of: the tree says it after the hook
//                   (edo.west.masa.1, then Gonroku's edo.west.gonroku.1 to .5), so the hook ends with her beside him and
//                   the family within earshot. (The tree sets edo.masaAsked before it and edo.west after: the beat of #24,
//                   the first leg's gate. The goodbyes, edo.west.bye.*, and the voyage are the scene's, after.)
//
// THE FACTS. Set by the trees: edo.tamiMet, edo.babySleeps, edo.clothes (#22's clothes), edo.clue.red (#21), edo.kiheiMet,
// edo.pennyShown, edo.clue.blue (#21; the scene sets it too, at the print), edo.kiheiWest (he has named the ship),
// edo.saidArigato, edo.catGone, edo.fed (#23's beat), edo.boxGiven, edo.sankichiMet, edo.boardRead, edo.arigato (she has
// the word), edo.bunsei, edo.dressed (#22's beat), edo.gonrokuMet, edo.gonrokuNo, edo.gonrokuWife (he has sent them to his
// wife), edo.masaMet, edo.masaAsked, edo.west (#24's beat). Set by the scenes, and read here: edo.clerkPassed (the first
// pass: O-Tami has had them in behind the noren), edo.clue.coins (the money box looked at: Big Sister's fact), edo.hensWest
// (Little Sister has seen the hens face west), edo.when (#21). And g.has("pennies") (the one talking has them),
// g.asked("<tree>/<option>"). S/work-20-writeA/ids.md says when each line is said.

const who = (g) => g.store.data.active;
const is = (g, fact) => !!g.flag(fact);
const lead = (g) => (["mom", "bigsis", "lilsis"].includes(who(g)) ? who(g) : "mom");
const node = (g) => ({ mom: "mom", bigsis: "big", lilsis: "lil" }[lead(g)]);

// ======================================================================================================
// tamiTree: O-Tami. The clothes (not until the baby sleeps: the lever is Mom with the baby), the baby, why her husband
// wears red (#21's first clue: a tiger year, the metal one), the clerk, and a word for the small one about the step.
// ======================================================================================================
export const tamiTree = (h = {}) => {
  const clothesNo = (id, line, say) => ({ id, line, clue: true, when: (g) => !is(g, "edo.babySleeps") && !is(g, "edo.clothes"), say });
  const clothesYes = (id, line) => ({ id, line, when: (g) => is(g, "edo.babySleeps") && !is(g, "edo.clothes"),
    say: ["edo.tami.clothes.yes"], then: async (g) => { if (h.dress) await h.dress(g); g.flag("edo.clothes", true); return "dressedNow"; } });
  const clothesDone = (id, line) => ({ id, line, once: true, when: (g) => is(g, "edo.clothes"), say: ["edo.tami.clothes.done"] });
  const red = (id, line) => ({ id, line, clue: true, say: ["edo.tami.red.1", "edo.tami.red.2", "edo.tami.red.3", "edo.tami.red.big"], set: "edo.clue.red" });
  const clerk = (id, line, say) => ({ id, line, clue: true, when: (g) => !is(g, "edo.dressed"), say });
  return {
    id: "tami",
    start: (g) => (is(g, "edo.tamiMet") ? node(g) : "first"),
    nodes: {
      first: { say: ["edo.tami.first.1"], then: (g) => { g.flag("edo.tamiMet", true); return node(g); } },
      mom: {
        options: [
          clothesNo("clothesMom", "edo.tami.opt.clothes.mom", ["edo.tami.clothes.no.1", "edo.tami.clothes.no.2"]),
          clothesYes("dressMom", "edo.tami.opt.clothes.mom"),
          clothesDone("dressedMom", "edo.tami.opt.clothes.mom"),
          // the baby: Mom's lever (the hook hums; the baby sleeps mid-sentence)
          { id: "babyMom", line: "edo.tami.opt.baby.mom", when: (g) => !is(g, "edo.babySleeps"),
            say: ["edo.shop.baby.1", "edo.shop.baby.2", "edo.shop.baby.3"],
            then: async (g) => { if (h.lullaby) await h.lullaby(g); g.flag("edo.babySleeps", true); return "slept"; } },
          { id: "babyDoneMom", line: "edo.tami.opt.baby.mom", once: true, when: (g) => is(g, "edo.babySleeps"), say: ["edo.tami.baby.done"] },
          red("redMom", "edo.tami.opt.red.mom"),
          clerk("clerkMom", "edo.tami.opt.clerk.mom", ["edo.tami.clerk.1", "edo.tami.clerk.2"]),
          { id: "byeMom", line: "edo.tami.opt.bye.mom", say: ["edo.tami.bye.mom"], then: "exit" },
        ],
      },
      big: {
        options: [
          clothesNo("clothesBig", "edo.tami.opt.clothes.big", ["edo.tami.clothes.no.1", "edo.tami.clothes.no.2"]),
          clothesYes("dressBig", "edo.tami.opt.clothes.big"),
          clothesDone("dressedBig", "edo.tami.opt.clothes.big"),
          { id: "babyBig", line: "edo.tami.opt.baby.big", once: true, when: (g) => !is(g, "edo.babySleeps"), say: ["edo.tami.baby.big"] },
          red("redBig", "edo.tami.opt.red.big"),
          clerk("clerkBig", "edo.tami.opt.clerk.big", ["edo.tami.clerk.1", "edo.tami.clerk.2"]),
          { id: "byeBig", line: "edo.tami.opt.bye.big", say: ["edo.tami.bye.big"], then: "exit" },
        ],
      },
      lil: {
        options: [
          clothesNo("clothesLil", "edo.tami.opt.clothes.lil", ["edo.tami.clothes.no.lil", "edo.tami.clothes.no.2"]),
          clothesYes("dressLil", "edo.tami.opt.clothes.lil"),
          clothesDone("dressedLil", "edo.tami.opt.clothes.lil"),
          { id: "babyLil", line: "edo.tami.opt.baby.lil", once: true, when: (g) => !is(g, "edo.babySleeps"), say: ["edo.tami.baby.lil", "edo.tami.baby.lil.2"] },
          red("redLil", "edo.tami.opt.red.lil"),
          clerk("clerkLil", "edo.tami.opt.clerk.lil", ["edo.tami.clerk.1", "edo.tami.clerk.lil"]),
          { id: "sushiLil", line: "edo.tami.opt.sushi.lil", clue: true, when: (g) => !is(g, "edo.fed"), say: ["edo.tami.sushi.lil"] },
          { id: "byeLil", line: "edo.tami.opt.bye.lil", say: ["edo.tami.bye.lil"], then: "exit" },
        ],
      },
      // asleep, in the middle of a sentence; O-Tami looks at Mom as at a sorceress, and remembers the chest
      slept: { say: ["edo.shop.baby.4", "edo.shop.baby.5", "edo.shop.baby.6"], then: "root" },
      // dressed (the hook said the lines of it): her last word sends them to the clerk
      dressedNow: { then: "root" },
    },
  };
};

// ======================================================================================================
// kiheiTree: Kihei. Sparse: "Sit." The price that is not a price (any of the three asking, or the pennies, or hunger,
// is the way to the meal), the red (ask my wife), the print in the new blue (#21), west and the ship (#24), the word, and
// "Okage-sama de". The meal is a chain of nodes with the scene's staging between them.
// ======================================================================================================
export const kiheiTree = (h = {}) => {
  const hook = (name, next) => async (g) => { if (h[name]) await h[name](g); return next; };
  const print = (id, line) => ({ id, line, clue: true, when: (g) => !is(g, "edo.when"),
    say: ["edo.kihei.print.1", "edo.kihei.print.2", "edo.shop.print.clue", "edo.shop.print.clue.2"], set: "edo.clue.blue" });
  const west = (id, line, say) => ({ id, line, clue: true, when: (g) => !is(g, "edo.west"), say, set: "edo.kiheiWest" });
  const WEST = ["edo.kihei.west.1", "edo.kihei.west.2", "edo.kihei.west.3", "edo.kihei.west.4"];
  return {
    id: "kihei",
    start: (g) => (is(g, "edo.kiheiMet") ? node(g) : "open"),
    nodes: {
      open: { say: ["edo.kihei.open"], then: (g) => { g.flag("edo.kiheiMet", true); return node(g); } },
      mom: {
        options: [
          { id: "priceMom", line: "edo.kihei.opt.price.mom", clue: true, when: (g) => !is(g, "edo.fed"), say: ["edo.kihei.price.1", "edo.kihei.price.2", "edo.kihei.price.3"], then: "meal" },
          { id: "redMom", line: "edo.kihei.opt.red.mom", clue: true, when: (g) => !is(g, "edo.clue.red"), say: ["edo.kihei.red"] },
          print("printMom", "edo.kihei.opt.print.mom"),
          west("westMom", "edo.kihei.opt.west.mom", WEST),
          { id: "thanksMom", line: "edo.kihei.opt.thanks.mom", once: true, when: (g) => is(g, "edo.fed"), say: ["edo.kihei.thanks.mom"] },
          { id: "byeMom", line: "edo.kihei.opt.bye.mom", say: ["edo.kihei.bye"], then: "exit" },
        ],
      },
      big: {
        options: [
          { id: "priceBig", line: "edo.kihei.opt.price.big", clue: true, when: (g) => !is(g, "edo.fed"), say: ["edo.kihei.price.big"], then: "meal" },
          { id: "redBig", line: "edo.kihei.opt.red.big", clue: true, when: (g) => !is(g, "edo.clue.red"), say: ["edo.kihei.red"] },
          print("printBig", "edo.kihei.opt.print.big"),
          west("westBig", "edo.kihei.opt.west.big", WEST),
          { id: "byeBig", line: "edo.kihei.opt.bye.big", say: ["edo.kihei.bye"], then: "exit" },
        ],
      },
      lil: {
        options: [
          { id: "hungryLil", line: "edo.kihei.opt.hungry.lil", clue: true, when: (g) => !is(g, "edo.fed"), say: ["edo.kihei.hungry.lil"], then: "meal" },
          // the pennies: no hole; he gives them back, and presses the sushi anyway
          { id: "penniesLil", line: "edo.kihei.opt.pennies.lil", when: (g) => g.has("pennies") && !is(g, "edo.pennyShown"),
            say: ["edo.shop.penny.1", "edo.shop.penny.2", "edo.shop.penny.3", "edo.shop.penny.4"], set: "edo.pennyShown", then: (g) => (is(g, "edo.fed") ? null : "meal") },
          { id: "redLil", line: "edo.kihei.opt.red.lil", clue: true, when: (g) => !is(g, "edo.clue.red"), say: ["edo.kihei.red.lil"] },
          west("westLil", "edo.kihei.opt.west.lil", ["edo.kihei.west.lil", "edo.kihei.west.1", "edo.kihei.west.3", "edo.kihei.west.4"]),
          // the word, brought back after the meal (if she had it at the table she has said it there)
          { id: "arigatoLil", line: "edo.kihei.opt.arigato.lil", once: true, when: (g) => is(g, "edo.arigato") && is(g, "edo.fed") && !is(g, "edo.saidArigato"),
            say: ["edo.shop.arigato.1", "edo.shop.arigato.2", "edo.shop.arigato.3"], set: "edo.saidArigato" },
          { id: "byeLil", line: "edo.kihei.opt.bye.lil", say: ["edo.kihei.bye.lil"], then: "exit" },
        ],
      },
      // ---- #23, the meal: the pressing (hook press), the step (serve), the grace and the bow (bow), the word, the title,
      // the cat (under), the box (giveBox). Nobody says itadakimasu.
      meal: { say: ["edo.shop.meal.1", "edo.shop.meal.2"], then: hook("press", "table") },
      table: { say: ["edo.shop.meal.3", "edo.shop.meal.4", "edo.shop.meal.5", "edo.shop.meal.6", "edo.shop.meal.7"], then: hook("serve", "grace") },
      grace: { say: ["edo.shop.meal.8", "edo.shop.meal.9"], then: hook("bow", "eat") },
      eat: { say: ["edo.shop.meal.10"], then: (g) => (is(g, "edo.arigato") ? "word" : "noword") },
      word: { say: ["edo.shop.meal.11", "edo.shop.meal.11.tami", "edo.shop.meal.11.kihei"], then: (g) => { g.flag("edo.saidArigato", true); return "thanks"; } },
      noword: { say: ["edo.shop.meal.11b"], then: "thanks" },
      thanks: { say: ["edo.shop.meal.12", "edo.shop.meal.13", "edo.shop.meal.14", "edo.shop.meal.15"], then: "cat" },
      cat: { say: ["edo.shop.meal.16", "edo.shop.meal.17", "edo.shop.meal.18"], then: async (g) => { if (h.under) await h.under(g); g.flag("edo.catGone", true); return "paid"; } },
      paid: { say: ["edo.shop.meal.19", "edo.shop.meal.20", "edo.shop.meal.21", "edo.shop.meal.22", "edo.shop.meal.23", "edo.shop.meal.24"],
        then: async (g) => { if (h.giveBox) await h.giveBox(g); g.flag("edo.fed", true); g.flag("edo.boxGiven", true); return is(g, "edo.arigato") ? "fedWord" : "exit"; } },
      fedWord: { say: ["edo.shop.meal.25"], then: "exit" },
    },
  };
};

// ======================================================================================================
// sankichiTree: Sankichi, nine, beside the board. The board, read once because somebody asked (and answered once); the
// year ("The thirteenth year of Bunsei": true, and no help, until it is); the word; questions back, in her rhythm.
// ======================================================================================================
export const sankichiTree = (h = {}) => {
  const READ = ["edo.village.board.read.1", "edo.village.board.read.2", "edo.village.board.read.3", "edo.village.board.read.4", "edo.village.board.read.4b"];
  const ANSWER = ["edo.village.board.read.5", "edo.village.board.read.6", "edo.village.board.read.7"];
  const board = (id, line) => ({ id, line, clue: true, when: (g) => !is(g, "edo.boardRead"),
    then: async (g) => { if (h.boardOpen) await h.boardOpen(g); return "reading"; } });
  const boardAgain = (id, line) => ({ id, line, when: (g) => is(g, "edo.boardRead"), once: true, say: ["edo.village.board.read.again"] });
  return {
    id: "sankichi",
    start: (g) => (is(g, "edo.sankichiMet") ? node(g) : { mom: "openMom", big: "openBig", lil: "openLil" }[node(g)]),
    nodes: {
      openLil: { say: ["edo.sankichi.open.lil", "edo.sankichi.open.lil.2", "edo.sankichi.open.lil.3", "edo.sankichi.open.lil.4"], then: (g) => { g.flag("edo.sankichiMet", true); return "lil"; } },
      openBig: { say: ["edo.sankichi.open.big", "edo.sankichi.open.big.2"], then: (g) => { g.flag("edo.sankichiMet", true); return "big"; } },
      openMom: { say: ["edo.sankichi.open.mom", "edo.sankichi.open.mom.2"], then: (g) => { g.flag("edo.sankichiMet", true); return "mom"; } },
      lil: {
        options: [
          board("boardLil", "edo.sankichi.opt.board.lil"),
          boardAgain("boardAgainLil", "edo.sankichi.opt.board.lil"),
          { id: "thanksLil", line: "edo.sankichi.opt.thanks.lil", clue: true, when: (g) => !is(g, "edo.arigato"),
            say: ["edo.sankichi.thanks.1", "edo.sankichi.thanks.2", "edo.sankichi.thanks.3"], set: "edo.arigato" },
          { id: "thanksAgainLil", line: "edo.sankichi.opt.thanks.lil", once: true, when: (g) => is(g, "edo.arigato"), say: ["edo.sankichi.thanks.again"] },
          { id: "questionsLil", line: "edo.sankichi.opt.questions.lil", once: true,
            say: ["edo.sankichi.questions.1", "edo.sankichi.questions.1b", "edo.sankichi.questions.2", "edo.sankichi.questions.3"] },
          { id: "bootsLil", line: "edo.sankichi.opt.boots.lil", once: true, say: ["edo.sankichi.boots", "edo.sankichi.boots.2"] },
          { id: "byeLil", line: "edo.sankichi.opt.bye.lil", say: ["edo.sankichi.bye.lil"], then: "exit" },
        ],
      },
      big: {
        options: [
          board("boardBig", "edo.sankichi.opt.board.big"),
          boardAgain("boardAgainBig", "edo.sankichi.opt.board.big"),
          { id: "yearBig", line: "edo.sankichi.opt.year.big", clue: true, when: (g) => !is(g, "edo.when"),
            say: ["edo.sankichi.year.1", "edo.sankichi.year.2", "edo.sankichi.year.3", "edo.sankichi.year.4"], set: "edo.bunsei" },
          { id: "schoolBig", line: "edo.sankichi.opt.school.big", once: true, say: ["edo.sankichi.school.1", "edo.sankichi.school.2"] },
          { id: "byeBig", line: "edo.sankichi.opt.bye.big", say: ["edo.sankichi.bye.big"], then: "exit" },
        ],
      },
      mom: {
        options: [
          board("boardMom", "edo.sankichi.opt.board.mom"),
          boardAgain("boardAgainMom", "edo.sankichi.opt.board.mom"),
          { id: "grandfatherMom", line: "edo.sankichi.opt.mom.mom", once: true, say: ["edo.sankichi.mom"] },
          { id: "byeMom", line: "edo.sankichi.opt.bye.mom", say: ["edo.sankichi.bye.mom"], then: "exit" },
        ],
      },
      // the reading, under the board's close-up; then the family's one answer; then the close-up away
      reading: { say: READ, then: (g) => { g.flag("edo.boardRead", true); return "answered"; } },
      answered: { say: ANSWER, then: async (g) => { if (h.boardClose) await h.boardClose(g); return "root"; } },
    },
  };
};

// ======================================================================================================
// tokuzoTree: Tokuzō, the headman's clerk. Before the kimonos the talk does not happen (O-Tami's hand on Mom's sleeve;
// or Little Sister's boots). Dressed: he peers, and asks, and every answer the player can pick is true. He writes
// "travellers, three, going west", and goes home, pleased: #22's end.
// ======================================================================================================
export const tokuzoTree = (h = {}) => ({
  id: "tokuzo",
  start: (g) => (is(g, "edo.dressed") ? "after" : !is(g, "edo.clothes") ? (lead(g) === "lilsis" ? "boots" : "notyet") : "open"),
  nodes: {
    notyet: { say: ["edo.tokuzo.notyet", "edo.tokuzo.notyet.2"] },
    boots: { say: ["edo.village.boots.lilsis", "edo.village.boots.mom"] },
    open: {
      say: ["edo.tokuzo.open.1"],
      options: [
        { id: "travellersMom", line: "edo.tokuzo.opt.travellers.mom", then: "from" },
        { id: "travellersBig", line: "edo.tokuzo.opt.travellers.big", then: "from" },
        { id: "travellersLil", line: "edo.tokuzo.opt.travellers.lil", say: ["edo.tokuzo.travellers.lil"], then: "from" },
      ],
    },
    from: {
      say: ["edo.tokuzo.from"],
      options: [
        { id: "fromBig", line: "edo.tokuzo.opt.from.big", say: ["edo.tokuzo.from.big", "edo.tokuzo.from.big.mom", "edo.tokuzo.from.big.2"], then: "tall" },
        { id: "fromMom", line: "edo.tokuzo.opt.from.mom", say: ["edo.tokuzo.from.mom"], then: "tall" },
        { id: "fromLil", line: "edo.tokuzo.opt.from.lil", say: ["edo.tokuzo.from.lil"], then: "tall" },
      ],
    },
    tall: {
      say: ["edo.tokuzo.tall"],
      options: [
        { id: "tallMom", line: "edo.tokuzo.opt.tall.mom", say: ["edo.tokuzo.tall.ans"], then: "write" },
        { id: "tallBig", line: "edo.tokuzo.opt.tall.big", say: ["edo.tokuzo.tall.ans"], then: "write" },
        { id: "tallLil", line: "edo.tokuzo.opt.tall.lil", say: ["edo.tokuzo.tall.ans"], then: "write" },
      ],
    },
    // he writes it down, and goes home, pleased; then the three of them (edo.dressed: the beat of #22)
    write: { say: ["edo.tokuzo.write.1", "edo.tokuzo.write.2", "edo.tokuzo.write.3"],
      then: async (g) => { g.flag("edo.dressed", true); if (h.home) await h.home(g); return "done"; } },
    done: { say: ["edo.dressed.1", "edo.dressed.2", "edo.dressed.3"], then: "exit" },
    // met again, if the scene keeps him on his rounds
    after: {
      say: ["edo.tokuzo.after"],
      options: [
        { id: "afterMom", line: "edo.tokuzo.after.opt.mom", say: ["edo.tokuzo.after.mom"], then: "exit" },
        { id: "afterLil", line: "edo.tokuzo.after.opt.lil", say: ["edo.tokuzo.after.lil"], then: "exit" },
      ],
    },
  },
});

// ======================================================================================================
// gonrokuTree: Gonroku, the captain, by his boat. No women aboard: the Funadama. Every argument fails, funnily, and he
// speaks in weather; the clue is his wife ("Mind how you ask."). The lever is a person, not an argument (masaTree).
// ======================================================================================================
export const gonrokuTree = (h = {}) => ({
  id: "gonroku",
  start: (g) => (is(g, "edo.west") ? "after" : is(g, "edo.gonrokuMet") ? "talk" : "greet"),
  nodes: {
    greet: { say: ["edo.gonroku.open"], then: (g) => { g.flag("edo.gonrokuMet", true); return "talk"; } },
    talk: {
      options: [
        { id: "passage", line: "edo.gonroku.opt.passage.mom", clue: true, say: ["edo.gonroku.no.1", "edo.gonroku.no.2", "edo.gonroku.no.3"], set: "edo.gonrokuNo" },
        { id: "hair", line: "edo.gonroku.opt.hair.big", once: true, when: (g) => g.asked("gonroku/passage") > 0, say: ["edo.gonroku.hair"] },
        { id: "luck", line: "edo.gonroku.opt.luck.lil", once: true, when: (g) => g.asked("gonroku/passage") > 0, say: ["edo.gonroku.luck"] },
        { id: "quiet", line: "edo.gonroku.opt.quiet.mom", once: true, when: (g) => g.asked("gonroku/passage") > 0, say: ["edo.gonroku.quiet"] },
        { id: "men", line: "edo.gonroku.opt.men.big", once: true, when: (g) => g.asked("gonroku/passage") > 0, say: ["edo.gonroku.men"] },
        { id: "stern", line: "edo.gonroku.opt.stern.lil", once: true, when: (g) => g.asked("gonroku/passage") > 0, say: ["edo.gonroku.stern"] },
        { id: "where", line: "edo.gonroku.opt.where.mom", clue: true, say: ["edo.gonroku.where"] },
        // the clue: his wife, at the nets, and how to ask her
        { id: "wife", line: "edo.gonroku.opt.wife.mom", clue: true, when: (g) => g.asked("gonroku/passage") > 0, say: ["edo.gonroku.wife"], set: "edo.gonrokuWife" },
        { id: "byeMom", line: "edo.gonroku.opt.bye.mom", say: ["edo.gonroku.bye.mom"], then: "exit" },
        { id: "byeBig", line: "edo.gonroku.opt.bye.big", say: ["edo.gonroku.bye.big"], then: "exit" },
        { id: "byeLil", line: "edo.gonroku.opt.bye.lil", say: ["edo.gonroku.bye.lil"], then: "exit" },
      ],
    },
    // after O-Masa has spoken: the terms, said once more
    after: {
      say: ["edo.gonroku.after.1"],
      options: [
        { id: "afterMom", line: "edo.gonroku.after.opt.mom", say: ["edo.gonroku.after.mom"], then: "exit" },
        { id: "afterLil", line: "edo.gonroku.after.opt.lil", say: ["edo.gonroku.after.lil"], then: "exit" },
      ],
    },
  },
});

// ======================================================================================================
// masaTree: O-Masa, at the net racks. Verdicts. A favour she gives her brother; a question she will take from anybody,
// properly asked, by someone dressed, fed, and passed by the clerk: then she goes down the beach, and the player hears
// the end of it. #24's lever, and the first leg's gate (edo.west).
// ======================================================================================================
export const masaTree = (h = {}) => ({
  id: "masa",
  start: (g) => (is(g, "edo.west") ? "after" : is(g, "edo.masaMet") ? "talk" : "greet"),
  nodes: {
    greet: { say: ["edo.masa.open"], then: (g) => { g.flag("edo.masaMet", true); return "talk"; } },
    talk: {
      options: [
        // the wrong foot that is the hint: a favour
        { id: "favour", line: "edo.masa.opt.favour.mom", clue: true, say: ["edo.masa.favour"] },
        { id: "unfair", line: "edo.masa.opt.unfair.big", once: true, say: ["edo.masa.unfair"] },
        { id: "boss", line: "edo.masa.opt.boss.lil", once: true, say: ["edo.masa.boss"] },
        { id: "nets", line: "edo.masa.opt.nets.lil", once: true, say: ["edo.masa.nets", "edo.masa.nets.2"] },
        { id: "brother", line: "edo.masa.opt.brother.mom", once: true, when: (g) => is(g, "edo.fed"), say: ["edo.masa.brother"] },
        { id: "lady", line: "edo.masa.opt.lady.big", once: true, say: ["edo.masa.lady"] },
        // the question, properly: her verdicts until they are ready (#22 and #23), and then the lever
        { id: "askNotDressed", line: "edo.masa.opt.ask.mom", clue: true, when: (g) => !is(g, "edo.clothes"), say: ["edo.masa.notdressed"] },
        { id: "askNotFed", line: "edo.masa.opt.ask.mom", clue: true, when: (g) => is(g, "edo.clothes") && !is(g, "edo.fed"), say: ["edo.masa.notfed"] },
        { id: "askNotClerk", line: "edo.masa.opt.ask.mom", clue: true, when: (g) => is(g, "edo.clothes") && is(g, "edo.fed") && !is(g, "edo.dressed"), say: ["edo.masa.notclerk"] },
        { id: "ask", line: "edo.masa.opt.ask.mom", when: (g) => is(g, "edo.dressed") && is(g, "edo.fed"),
          say: ["edo.masa.ask.1", "edo.masa.ask.2", "edo.masa.ask.3", "edo.masa.ask.4"], set: "edo.masaAsked",
          then: async (g) => { if (h.toGonroku) await h.toGonroku(g); return "verdict"; } },
        { id: "byeMom", line: "edo.masa.opt.bye.mom", say: ["edo.masa.bye.mom"], then: "exit" },
        { id: "byeBig", line: "edo.masa.opt.bye.big", say: ["edo.masa.bye.big"], then: "exit" },
        { id: "byeLil", line: "edo.masa.opt.bye.lil", say: ["edo.masa.bye.lil"], then: "exit" },
      ],
    },
    // down the beach: what the player hears the end of; Gonroku, after a long look at the sea; the terms
    verdict: { say: ["edo.west.masa.1", "edo.west.gonroku.1", "edo.west.gonroku.2", "edo.west.gonroku.3", "edo.west.gonroku.4", "edo.west.gonroku.5"],
      then: (g) => { g.flag("edo.west", true); return "exit"; } },
    after: { say: ["edo.masa.after"], then: "exit" },
  },
});

/** Every tree, by name, for the tests. */
export const trees = { tamiTree, kiheiTree, sankichiTree, tokuzoTree, gonrokuTree, masaTree };

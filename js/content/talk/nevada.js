// The talks of Act Four (Nevada, expanded) and of Act Five's opening, as dialogue trees (NEVADA-12W: new in round
// twelve; briefs/WRITE-12.md). Plain data in the engine's format (docs/DESIGN.md, section 7, "Dialogue trees"):
// every word is a line id (js/content/lines/nevada.en.js and limo.en.js). An option's `line` is said by the one who
// picks it; its `say` is the reply (a list, or { 1, 2, more } by how many times it has been asked); `set` makes facts
// true; `do` is a script; `then` goes to a node, "back", "root" or "exit" (or is a function of the game giving one).
//
// Each tree is a function of a `hooks` object, so that the scene hands in the scripts a branch needs:
//     import { joeTree } from "../talk/nevada.js";
//     const JOE = joeTree({ witness, lemonade, coinTold, play, banjo, banjoDone, hold });
//     ...  use: (g) => g.talk(JOE)
// A hook that is not handed in is skipped (the talk still says every line and sets every fact).
//
// THE HOOKS, and what each must do. None of them may say a line the tree says; those that say lines say them here.
//   joeTree (Grandpa Joe, on the porch)
//     lemonade(g)   Mom has bought three lemonades: he gets up, pours three at the stand, sits back down. Staging only.
//     witness(g)    the right car is named and the story told (the tree said it): he looks up the road toward the
//                   glass, a hand to his hat. Staging only (the tree sets nevada.storyTold).
//     coinTold(g)   after "He don't steal. He trades.": he tips his hat (the dent), and Ranger, on the chair's arm,
//                   folds his hands and looks at Mom. Staging only (the tree sets nevada.witness: the beat of #5).
//     play(g)       he plays a few bars of the Last Stop Rag in the low sun, and the chrome back of the banjo flashes
//                   (the tune is the game's own). Staging and music; no lines.
//     banjo(g)      #12's half-answer: he gets up, walks to the glass (HOLD), and plays facing the sun: the door grows
//                   from a coin to a banjo, and stays that size while he plays. (The tree sets nevada.banjoTried.)
//     banjoDone(g)  he stops; the door shuts back to a coin, and the music with it; he walks back and sits down.
//     hold(g)       #12's answer: he gets up out of the rocker, slowly, a hand to the small of his back, takes the sun
//                   shade (g.take from whichever of the three has it), walks to HOLD and holds it square to the sun:
//                   the door grows from the coin to a windshield's width. Must set nevada.wideOpen.
//   joleneTree (Grandma Jolene, behind the counter)
//     giveShade(g)  she lifts the sun shade out of the window (the cut-out goes) and it goes into the pockets of
//                   whoever asked (g.give("storeshade")). (The tree sets nevada.shadeGiven.)
//     phone(g)      she picks up the dead pay phone's receiver as she answers it, and hangs it up after. Staging.
//     out(g)        Little Sister goes out of the back door onto the step (mark `step`), the other two to the doorway;
//                   the first time, Jolene says nevada.jolene.names from the doorway. Then the scene runs hensTree.
//   rangerTree (Ranger, on the porch: Grandpa Joe says what he means)
//     trade(g)      #10: Big Sister holds the mirror shades out flat on both hands and keeps still; Ranger takes them,
//                   turns them over, looks at himself in both lenses, scampers into the store and back, and puts the
//                   coin in her hand; then he puts the shades on (the `shades` variant). Must take "mirrorshades"
//                   from her, give her "coin", and set nevada.traded.
//     tail(g)       Ranger turns round and shows her his tail. Staging.
//     snatch(g)     Little Sister holds the mirror shades out; Ranger reaches; she snatches them back. Staging (the
//                   tree then says her line, and calls tail).
//   hensTree (Little Sister on the back step, the hens before her)
//     row(g)        she steps down into the row with the hens and faces the fence.
//     sit(g, n)     hen n sits down (1 Darlene, 2 Charlene). The others stay on guard.
//     egg(g)        Darlene lays an egg, right there in the dust.
//     giveEgg(g)    the egg is Little Sister's: g.give("egg"). (The tree sets nevada.jolene: the beat of #11.)
//   letterboxTree (through the coin door: g.talk(letterboxTree(h), { through: "son" }))
//     penny(g)      Little Sister pushes her lucky penny into the door for her brother: g.send("penny", { to: "son" }),
//                   and the door winks. Must set nevada.pennySent.
//     (LETTER-17, round seventeen: the night Mom hears her son. Staging, all of them; none says a line.)
//     kneel(g)      his voice: whoever was speaking into the door makes room, Mom's handbag goes down on the gravel, and
//                   she is at the door on her knees, facing it (figure.kneel). It is started at his first line and awaited
//                   after the hello of the two of them: it gives back a promise of her being down. Must set nevada.bagDown.
//     heels(g)      she understands: she sits back on her heels, and the girls come and stand either side of her.
//     lean(g)       she leans in to the door again (kneels up), to ask if he has eaten.
//     rise(g)       the end of the warning: she gets up off her knees.
//     turn(g)       Grandpa Joe has said "Ma'am.": she turns to him, and he to her.
//     bring(g)      Ranger comes from beside the rocker to the handbag on the gravel, picks it up, and holds it up to her.
//     take(g)       she bends and takes it: the handbag is on her arm again. Must set nevada.bagDown false.
//   dividerTree (Act Five: Grandpa Joe, to the divider while it is down)
//     sing(g)       after he has started humming (the tree says the hum): the divider slides up and stays up while
//                   he sings. Must set the scene's fact for the divider being up.
//
// THE FACTS the `when`s read (S/work-writer/ids.md says who sets each). Set by the trees: nevada.joeLiked,
// nevada.rangerMet, nevada.vegas, nevada.vegasTwice, nevada.lemonade, nevada.storyTold, nevada.hensTold, nevada.witness,
// nevada.joeLilAfter, nevada.banjoFlash, nevada.banjoTried, nevada.shadeGiven, nevada.factsTold (a number),
// nevada.jolene, nevada.sonMet, nevada.sonPinned, nevada.heardSon. Set by the scenes and hooks: nevada.visits (a number),
// nevada.doorOpen (#9), nevada.wideOpen (#12), nevada.traded (#10), nevada.pennies (she has taken the pennies),
// nevada.pennySent, and (LETTER-17) nevada.bagDown (Mom's handbag on the gravel: from her kneeling at the little door to
// Ranger bringing it back). And g.has("mirrorshades"), g.has("penny") (the one talking has it), and g.asked("<tree>/<option>").

const who = (g) => g.store.data.active;
const is = (g, fact) => !!g.flag(fact);
const visits = (g) => g.flag("nevada.visits") || 0;
const factsTold = (g) => g.flag("nevada.factsTold") || 0;

// ======================================================================================================
// joeTree: Grandpa Joe. #5 (Ask Nicely), and after: the asking, the flash again, the hens, the coin, the banjo asked
// for, the hubcaps, the sun shade held, and the ways out. Mom has four ways in; each of the girls has her own talk.
// ======================================================================================================
export const joeTree = (h = {}) => ({
  id: "joe",
  start: (g) => {
    if (who(g) === "lilsis") return is(g, "nevada.witness") && !is(g, "nevada.joeLilAfter") ? "lilAfter" : "lil";
    if (who(g) === "bigsis") return "big";
    if (is(g, "nevada.storyTold")) return "after";
    if (is(g, "nevada.joeLiked") || is(g, "nevada.lemonade")) return "asking";
    return "open";
  },
  nodes: {
    // ---- Mom walks up. He does not look up. Ranger does. Four ways in: the way in, the trade first, the lever, the laugh.
    open: {
      options: [
        { id: "morning", line: "nevada.joe.opt.morning", set: "nevada.joeLiked", then: "morning" },
        { id: "lemonade", line: "nevada.joe.opt.lemonade", when: (g) => !is(g, "nevada.vegasTwice"), say: ["nevada.joe.lemonade.1", "nevada.joe.lemonade.lilsis"], set: "nevada.lemonade", do: h.lemonade, then: "asking" },
        { id: "lemonade2", line: "nevada.joe.opt.lemonade", when: (g) => is(g, "nevada.vegasTwice"), say: ["nevada.joe.lemonade.2", "nevada.joe.lemonade.lilsis"], set: "nevada.lemonade", do: h.lemonade, then: "asking" },
        { id: "raccoon", line: "nevada.joe.opt.raccoon", set: ["nevada.joeLiked", "nevada.rangerMet"], then: "ranger" },
        { id: "vegas", line: "nevada.joe.opt.vegas", say: { 1: ["nevada.joe.vegas.1", "nevada.joe.vegas.2"], 2: ["nevada.joe.vegas.again"], more: ["nevada.joe.vegas.more"] },
          set: "nevada.vegas", then: (g) => (g.asked("joe/vegas") === 1 ? "vegas" : null) },
        { id: "leave", line: "nevada.ask.bye", say: ["nevada.joe.bye.1"], then: "exit" },
      ],
    },
    morning: {
      say: ["nevada.old.mom.2"],
      options: [
        { id: "people", line: "nevada.joe.opt.people", say: ["nevada.joe.people"] },
        { id: "never", line: "nevada.joe.opt.never", once: true, when: (g) => g.asked("joe/people") > 0, say: ["nevada.joe.never"] },
        { id: "time", line: "nevada.joe.opt.time", when: (g) => !is(g, "nevada.vegasTwice"), say: ["nevada.joe.time"], then: "asking" },
        { id: "timeVegas", line: "nevada.joe.opt.time", when: (g) => is(g, "nevada.vegasTwice"), say: ["nevada.joe.time.vegas"], then: "asking" },
      ],
    },
    ranger: {
      say: ["nevada.joe.ranger.1", "nevada.ranger.dots", "nevada.joe.ranger.2", "nevada.ranger.dots", "nevada.joe.ranger.3"],      // PASS-17N: a second translation (the handbag)
      options: [
        { id: "always", line: "nevada.joe.opt.always", say: ["nevada.joe.always"] },
        { id: "eat", line: "nevada.joe.opt.eat", say: ["nevada.joe.eat"] },                     // the clue: shiny, he keeps
        { id: "yesterday", line: "nevada.joe.opt.yesterday", then: "asking" },
      ],
    },
    vegas: {
      options: [
        { id: "testing", line: "nevada.joe.opt.testing", say: ["nevada.joe.passed"], then: "root" },
        { id: "though", line: "nevada.joe.opt.though", say: ["nevada.joe.jolene", "nevada.jolene.double", "nevada.joe.surcharge"], set: "nevada.vegasTwice", then: "root" },
      ],
    },
    // ---- the asking: he tells the story only to someone who has said good morning (or admired his raccoon)
    asking: {
      options: [
        { id: "car", line: "nevada.joe.opt.car", when: (g) => is(g, "nevada.joeLiked"), say: ["nevada.old.mom.5", "nevada.old.mom.6", "nevada.old.mom.7"], then: "cars" },
        { id: "carNo", line: "nevada.joe.opt.car", when: (g) => !is(g, "nevada.joeLiked"), say: ["nevada.old.bigsis.2"] },
        { id: "gray", line: "nevada.joe.opt.gray", say: ["nevada.old.mom.3", "nevada.joe.gray.2"], then: "gray" },          // the cheeseburger starts here
        { id: "gas", line: "nevada.joe.opt.gas", say: { 1: ["nevada.joe.gas.1"], 2: ["nevada.joe.gas.2"], more: ["nevada.joe.gas.3"] } },
        { id: "manners", line: "nevada.joe.opt.manners", when: (g) => !is(g, "nevada.joeLiked"), set: "nevada.joeLiked", then: "morning" },
        { id: "raccoon2", line: "nevada.joe.opt.raccoon", when: (g) => !is(g, "nevada.rangerMet"), set: ["nevada.joeLiked", "nevada.rangerMet"], then: "ranger" },
        { id: "lemonadeMore", line: "nevada.joe.opt.lemonade", when: (g) => is(g, "nevada.lemonade"), say: ["nevada.joe.lemonade.again"] },
        { id: "bye", line: "nevada.ask.bye", say: { 1: ["nevada.joe.bye.1"], 2: ["nevada.ans.bye"], more: ["nevada.joe.bye.3"] }, then: "exit" },
      ],
    },
    gray: {
      options: [
        { id: "nothing", line: "nevada.old.mom.4", when: (g) => is(g, "nevada.joeLiked"), say: ["nevada.old.mom.5", "nevada.old.mom.6", "nevada.old.mom.7"], then: "cars" },
        { id: "nothingNo", line: "nevada.old.mom.4", when: (g) => !is(g, "nevada.joeLiked"), say: ["nevada.joe.gray.stranger"] },
        { id: "breakfast", line: "nevada.joe.opt.breakfast", say: ["nevada.joe.breakfast"] },
        { id: "grayBack", line: "nevada.joe.opt.back", then: "back" },
      ],
    },
    // ---- "Then tell me what they were driving." A wrong answer costs a line, and he asks again.
    cars: {
      options: [
        { id: "sedan", line: "nevada.car.sedan", say: ["nevada.car.no.sedan"] },
        { id: "wagon", line: "nevada.car.wagon", say: ["nevada.old.saw.1", "nevada.old.saw.1b", "nevada.old.saw.2", "nevada.old.saw.3"], set: "nevada.storyTold", do: h.witness, then: "after" },
        { id: "black", line: "nevada.car.black", say: ["nevada.car.no.black"] },
      ],
    },
    // ---- after the story: the flash again, the strange week (first the hens, then the coin: he likes the order), and the rest
    after: {
      options: [
        { id: "flash", line: "nevada.ask.flash", say: ["nevada.ans.flash"] },
        { id: "week1", line: "nevada.joe.opt.week", when: (g) => !is(g, "nevada.hensTold"), say: ["nevada.old.saw.3b", "nevada.joe.hens.banjo", "nevada.old.saw.3c"], set: "nevada.hensTold" },
        { id: "week2", line: "nevada.joe.opt.week", when: (g) => is(g, "nevada.hensTold") && !is(g, "nevada.witness"),
          say: ["nevada.old.saw.5", "nevada.old.saw.5b", "nevada.old.saw.6", "nevada.old.saw.7"], set: ["nevada.witness", "nevada.rangerMet"], do: h.coinTold, then: "coin" },
        { id: "week3", line: "nevada.joe.opt.week", when: (g) => is(g, "nevada.witness"), say: ["nevada.joe.week.done"] },
        { id: "tradeAgain", line: "nevada.joe.opt.trade", when: (g) => is(g, "nevada.witness") && !is(g, "nevada.traded"), say: ["nevada.old.saw.8"] },
        { id: "fence", line: "nevada.ask.fence", say: ["nevada.ans.fence"] },
        { id: "areas", line: "nevada.ask.areas", say: ["nevada.ans.areas"] },
        { id: "grayAfter", line: "nevada.joe.opt.gray", say: ["nevada.old.mom.3", "nevada.joe.gray.2"], then: "grayAfter" },
        { id: "hubcaps", line: "nevada.joe.opt.hubcaps", when: (g) => visits(g) > 0, say: ["nevada.joe.hubcaps"] },
        { id: "laying", line: "nevada.joe.opt.laying", once: true, when: (g) => is(g, "nevada.jolene"), say: ["nevada.joe.laying"] },
        // #12: the banjo, asked for nicely (the half-answer), and then the sun shade, held
        { id: "banjo", line: "nevada.shade.banjo.ask", when: (g) => is(g, "nevada.doorOpen") && !is(g, "nevada.banjoTried"), say: ["nevada.shade.banjo.1"],
          set: "nevada.banjoTried", do: h.banjo, then: "banjo" },
        { id: "hold", line: "nevada.shade.ask", when: (g) => is(g, "nevada.shadeGiven") && is(g, "nevada.doorOpen") && !is(g, "nevada.wideOpen"),
          say: ["nevada.shade.need", "nevada.shade.joe"], do: h.hold, then: "wide" },
        { id: "byeAfter", line: "nevada.ask.bye", say: { 1: ["nevada.ans.bye"], more: ["nevada.joe.bye.3"] }, then: "exit" },
      ],
    },
    coin: {
      options: [
        { id: "trade", line: "nevada.joe.opt.trade", say: ["nevada.old.saw.8"] },                // his hint for #10
        { id: "hat", line: "nevada.joe.opt.hat", say: ["nevada.joe.hat"] },
        { id: "thanks", line: "nevada.old.saw.4", say: ["nevada.joe.welcome"], then: "after" },
      ],
    },
    grayAfter: {
      options: [
        { id: "breakfast2", line: "nevada.joe.opt.breakfast", say: ["nevada.joe.breakfast"] },
        { id: "grayAfterBack", line: "nevada.joe.opt.back", then: "back" },
      ],
    },
    banjo: {
      say: ["nevada.shade.banjo.fit", "nevada.shade.banjo.no", "nevada.shade.banjo.sideways", "nevada.shade.banjo.no", "nevada.shade.banjo.bigsis"],
      options: [
        { id: "banjoThanks", line: "nevada.shade.banjo.thanks", say: ["nevada.shade.banjo.joe"], do: h.banjoDone, then: "exit" },
      ],
    },
    wide: { say: ["nevada.shade.open.lilsis", "nevada.shade.open.bigsis", "nevada.shade.open.mom"], then: "exit" },

    // ---- Little Sister and Grandpa Joe
    lilAfter: { say: ["nevada.old.after.lilsis.1", "nevada.old.after.lilsis.2"], then: (g) => { g.flag("nevada.joeLilAfter", true); return "lil"; } },
    lil: {
      options: [
        { id: "daddy", line: "nevada.old.lilsis.1", when: (g) => !is(g, "nevada.witness"), say: ["nevada.old.lilsis.2", "nevada.old.lilsis.3"] },
        { id: "grandpa", line: "nevada.joe.opt.grandpa", say: { 1: ["nevada.joe.grandpa.1", "nevada.joe.grandpa.2", "nevada.joe.grandpa.3", "nevada.joe.grandpa.4"], more: ["nevada.joe.grandpa.again"] } },
        { id: "raccoonLil", line: "nevada.joe.opt.raccoon.lil", say: ["nevada.joe.raccoon.lil", "nevada.ranger.dots", "nevada.joe.raccoon.lil.2"], set: "nevada.rangerMet" },
        { id: "play", line: "nevada.joe.opt.play", say: { 1: ["nevada.joe.play.1"], 2: ["nevada.joe.play.2"], more: ["nevada.joe.play.more"] }, set: "nevada.banjoFlash",
          do: h.play, then: (g) => (g.asked("joe/play") === 1 ? "played" : null) },
        { id: "banjoLil", line: "nevada.joe.opt.banjo.lil", when: (g) => is(g, "nevada.doorOpen") && !is(g, "nevada.banjoTried"), say: ["nevada.joe.banjo.lil"] },
        { id: "lilBye", line: "nevada.joe.opt.lilbye", say: ["nevada.joe.lilbye"], then: "exit" },
      ],
    },
    played: { say: ["nevada.joe.play.lilsis", "nevada.joe.play.flash"], then: "root" },

    // ---- Big Sister and Grandpa Joe: the cross-examination is a choice
    big: {
      options: [
        { id: "observe", line: "nevada.old.bigsis.1", when: (g) => !is(g, "nevada.witness"), say: ["nevada.old.bigsis.2"], then: "double" },
        { id: "raccoonBig", line: "nevada.joe.opt.raccoon.big", say: ["nevada.joe.raccoon.big", "nevada.ranger.dots", "nevada.joe.raccoon.big.2"] },      // PASS-17N: and Ranger answers back
        { id: "geiger", line: "nevada.old.after.bigsis.1", when: (g) => is(g, "nevada.witness"), say: ["nevada.old.after.bigsis.2", "nevada.old.after.bigsis.3"] },
        { id: "banjoBig", line: "nevada.joe.opt.banjo.big", when: (g) => is(g, "nevada.doorOpen") && !is(g, "nevada.banjoTried"), say: ["nevada.joe.banjo.big"] },
        { id: "bigBye", line: "nevada.joe.opt.bigbye", say: ["nevada.joe.bigbye"], then: "exit" },
      ],
    },
    double: {
      options: [
        { id: "technically", line: "nevada.old.bigsis.3", say: ["nevada.old.bigsis.4", "nevada.joe.big.note"], then: "root" },
        { id: "oath", line: "nevada.joe.opt.oath", say: ["nevada.joe.oath"] },
        { id: "bigBack", line: "nevada.joe.opt.bigback", say: ["nevada.joe.bigback"], then: "exit" },
      ],
    },
  },
});

// ======================================================================================================
// joleneTree: Grandma Jolene, behind the counter. The hens, the window, her facts (one a visit, each put right by Big
// Sister), Joe, the gray fella, the hats, the phone. Little Sister and she talk chickens like two colleagues.
// ======================================================================================================
const fact = (n) => ({ say: FACTS[n], then: (g) => { g.flag("nevada.factsTold", n); return "back"; } });
const FACTS = {
  1: ["nevada.jolene.fact.1", "nevada.jolene.fact.1b", "nevada.jolene.fact.1c", "nevada.jolene.fact.1d"],
  2: ["nevada.jolene.fact.2", "nevada.jolene.fact.2b", "nevada.jolene.fact.2c", "nevada.jolene.fact.2d"],
  3: ["nevada.jolene.fact.3", "nevada.jolene.fact.3b", "nevada.jolene.fact.3c"],
  4: ["nevada.jolene.fact.4", "nevada.jolene.fact.4b", "nevada.jolene.fact.4c", "nevada.jolene.fact.4d"],
};
/** Her next fact is ready: one a visit, four in all. */
const factReady = (g) => factsTold(g) < Math.min(4, visits(g));
const nextFact = (g) => "fact" + (factsTold(g) + 1);
/** The window: not for sale (it is a shed without it), anything but the window, do somethin' about my girls; then hers to give. */
const windowAsk = (id, line) => ({ id, line, when: (g) => !is(g, "nevada.jolene") && !is(g, "nevada.shadeGiven"),
  say: { 1: ["nevada.jolene.window.1"], 2: ["nevada.jolene.window.2"], more: ["nevada.jolene.window.3"] } });
const windowGive = (h, id, line) => ({ id, line, when: (g) => is(g, "nevada.jolene") && !is(g, "nevada.shadeGiven"),
  say: ["nevada.jolene.window.give"], set: "nevada.shadeGiven", do: h.giveShade });

export const joleneTree = (h = {}) => {
  return {
    id: "jolene",
    start: (g) => (who(g) === "bigsis" ? "big" : who(g) === "lilsis" ? "lil" : "mom"),
    nodes: {
      mom: {
        options: [
          { id: "hensMom", line: "nevada.jolene.opt.hens.mom", say: ["nevada.jolene.hens.1"], then: "hensMom" },
          windowAsk("windowMom", "nevada.jolene.opt.window.mom"),
          windowGive(h, "giveMom", "nevada.jolene.opt.window.mom"),
          { id: "factMom", line: "nevada.jolene.opt.fact.mom", when: factReady, then: nextFact },
          { id: "joeMom", line: "nevada.jolene.opt.joe.mom", say: ["nevada.jolene.joe.1"] },
          { id: "grayMom", line: "nevada.jolene.opt.gray.mom", say: ["nevada.jolene.grill.1", "nevada.jolene.grill.2", "nevada.jolene.gray.3"] },
          { id: "hatsMom", line: "nevada.jolene.opt.hats.mom", say: ["nevada.jolene.hats"] },
          { id: "phoneMom", line: "nevada.jolene.opt.phone.mom", say: ["nevada.jolene.phone.1", "nevada.jolene.phone.2"], do: h.phone },
          { id: "byeMom", line: "nevada.jolene.opt.bye.mom", say: ["nevada.jolene.bye.mom"], then: "exit" },
        ],
      },
      hensMom: {
        options: [
          { id: "atWhat", line: "nevada.jolene.opt.atwhat", say: ["nevada.jolene.hens.2"] },
          { id: "namesMom", line: "nevada.jolene.opt.names.mom", say: ["nevada.jolene.names"] },
          { id: "poor", line: "nevada.jolene.opt.poor", then: "back" },
        ],
      },
      big: {
        options: [
          { id: "hensBig", line: "nevada.jolene.opt.hens.big", once: true, say: ["nevada.jolene.frightened", "nevada.jolene.fair"] },
          windowAsk("windowBig", "nevada.jolene.opt.window.big"),
          windowGive(h, "giveBig", "nevada.jolene.opt.window.big"),
          { id: "factBig", line: "nevada.jolene.opt.fact.big", when: factReady, then: nextFact },
          { id: "joeBig", line: "nevada.jolene.opt.joe.big", say: ["nevada.jolene.joe.2"] },
          { id: "grayBig", line: "nevada.jolene.opt.gray.big", say: ["nevada.jolene.grill.1", "nevada.jolene.grill.2", "nevada.jolene.gray.3"] },
          { id: "hatsBig", line: "nevada.jolene.opt.hats.big", say: ["nevada.jolene.hats.big"] },
          { id: "phoneBig", line: "nevada.jolene.opt.phone.big", say: ["nevada.jolene.phone.1", "nevada.jolene.phone.2"], do: h.phone },
          { id: "byeBig", line: "nevada.jolene.opt.bye.big", say: ["nevada.jolene.bye.big"], then: "exit" },
        ],
      },
      lil: {
        options: [
          // the colleagues' branch: what do you feed yours?
          { id: "hensLil", line: "nevada.jolene.opt.hens.lil", say: ["nevada.jolene.flock", "nevada.jolene.feed.lil", "nevada.jolene.color", "nevada.jolene.blue.lil", "nevada.jolene.blue"], then: "hensLil" },
          windowAsk("windowLil", "nevada.jolene.opt.window.lil"),
          windowGive(h, "giveLil", "nevada.jolene.opt.window.lil"),
          { id: "factLil", line: "nevada.jolene.opt.fact.lil", when: factReady, then: nextFact },
          { id: "joeLil", line: "nevada.jolene.opt.joe.lil", say: ["nevada.jolene.joe.lil"] },
          { id: "grayLil", line: "nevada.jolene.opt.gray.lil", say: ["nevada.jolene.gray.lil"] },
          { id: "hatsLil", line: "nevada.jolene.opt.hats.lil", say: ["nevada.jolene.hats"] },
          { id: "phoneLil", line: "nevada.jolene.opt.phone.lil", say: ["nevada.jolene.phone.1", "nevada.jolene.phone.2"], do: h.phone },
          { id: "byeLil", line: "nevada.jolene.opt.bye.lil", say: ["nevada.jolene.bye.lil"], then: "exit" },
        ],
      },
      hensLil: {
        options: [
          { id: "namesLil", line: "nevada.jolene.opt.names.lil", say: ["nevada.jolene.names", "nevada.jolene.names.lil"] },
          { id: "askHens", line: "nevada.jolene.opt.ask.lil", when: (g) => !is(g, "nevada.jolene"), say: ["nevada.jolene.ask"], do: h.out, then: "exit" },
          { id: "later", line: "nevada.jolene.opt.later.lil", then: "back" },
        ],
      },
      fact1: fact(1), fact2: fact(2), fact3: fact(3), fact4: fact(4),
    },
  };
};

// ======================================================================================================
// rangerTree: Ranger, on the porch. He says "..."; Grandpa Joe says what he means, and Little Sister does both parts.
// One tree, whose start reads who is talking. #10's trade is Big Sister's, with the mirror shades.
// ======================================================================================================
export const rangerTree = (h = {}) => ({
  id: "ranger",
  start: (g) => (who(g) === "bigsis" ? "big" : who(g) === "lilsis" ? "lil" : "mom"),
  nodes: {
    mom: {
      options: [
        { id: "morningR", line: "nevada.ranger.opt.morning", say: ["nevada.ranger.dots", "nevada.ranger.morning.joe"] },
        { id: "coinMom", line: "nevada.ranger.opt.coin.mom", when: (g) => is(g, "nevada.witness") && !is(g, "nevada.traded"), say: ["nevada.ranger.dots", "nevada.ranger.mom.no", "nevada.ranger.mom.joe"] },
        { id: "suit", line: "nevada.ranger.opt.suit", when: (g) => is(g, "nevada.traded"), say: ["nevada.ranger.dots", "nevada.ranger.suit.joe"] },
        { id: "byeMomR", line: "nevada.ranger.opt.bye.mom", say: { 1: ["nevada.ranger.dots", "nevada.ranger.carry.joe"], more: ["nevada.ranger.dots"] }, then: "exit" },      // PASS-17N: and what he means (once)
      ],
    },
    big: {
      options: [
        { id: "latin", line: "nevada.ranger.opt.latin", once: true, say: ["nevada.ranger.dots", "nevada.ranger.latin.joe"] },
        { id: "coinBig", line: "nevada.ranger.opt.coin.big", when: (g) => is(g, "nevada.witness") && !is(g, "nevada.traded"), say: ["nevada.ranger.dots", "nevada.ranger.coin.joe"] },
        // #10: the fact, the method, and the trade
        { id: "trade", line: "nevada.ranger.opt.trade", when: (g) => g.has("mirrorshades") && !is(g, "nevada.traded"), say: ["nevada.ranger.fact", "nevada.ranger.method"], do: h.trade, then: "traded" },
        { id: "bargain", line: "nevada.ranger.opt.big.after", when: (g) => is(g, "nevada.traded"), say: ["nevada.ranger.dots", "nevada.ranger.after.joe"] },
        { id: "byeBigR", line: "nevada.ranger.opt.bye.big", say: { 1: ["nevada.ranger.dots", "nevada.ranger.dismissed.joe"], more: ["nevada.ranger.dots"] }, then: "exit" },      // PASS-17N: and what he means (once)
      ],
    },
    traded: { say: ["nevada.ranger.thanks", "nevada.ranger.lil.good", "nevada.ranger.big.fast"], then: "exit" },
    // Little Sister's long conversation, in which she does both parts
    lil: {
      options: [
        { id: "hi", line: "nevada.ranger.opt.hi", when: (g) => !is(g, "nevada.rangerMet"), say: ["nevada.ranger.dots", "nevada.ranger.hi.2"], set: "nevada.rangerMet" },
        { id: "color", line: "nevada.ranger.opt.color", say: ["nevada.ranger.dots", "nevada.ranger.color.2"] },                  // the clue: SHINY
        { id: "chickens", line: "nevada.ranger.opt.chickens", say: ["nevada.ranger.dots", "nevada.ranger.chickens.2"] },
        { id: "wash", line: "nevada.ranger.opt.wash", say: ["nevada.ranger.dots", "nevada.ranger.wash.2"] },
        // PASS-17N: her spare grandpa comes round once more (once she has asked Grandpa Joe for one)
        { id: "spare", line: "nevada.ranger.opt.spare", once: true, when: (g) => g.asked("joe/grandpa") > 0, say: ["nevada.ranger.dots", "nevada.ranger.spare.2"] },
        { id: "coinLil", line: "nevada.ranger.opt.coin.lil", when: (g) => is(g, "nevada.witness") && !is(g, "nevada.traded"),
          say: ["nevada.ranger.lil.evidence", "nevada.ranger.dots"], do: h.tail, then: "noLil" },
        { id: "shadesLil", line: "nevada.ranger.opt.shades.lil", when: (g) => g.has("mirrorshades") && !is(g, "nevada.traded"), do: h.snatch, then: "holder" },
        { id: "shades2", line: "nevada.ranger.opt.shades2", when: (g) => is(g, "nevada.traded"), say: ["nevada.ranger.dots", "nevada.ranger.shades2.2"] },
        { id: "byeLilR", line: "nevada.ranger.opt.bye.lil", say: ["nevada.ranger.bye.joe"], then: "exit" },
      ],
    },
    noLil: { say: ["nevada.ranger.no.lil"], then: "root" },
    holder: { say: ["nevada.ranger.lil.holder"], then: async (g) => { if (h.tail) await h.tail(g); return "manners"; } },
    manners: { say: ["nevada.ranger.manners"], then: "root" },
  },
});

// ======================================================================================================
// hensTree: #11, Jolene's Girls. Little Sister on the back step. What she tries first is the player's choice; the
// order she names them in is hers (Darlene, Charlene, then the other three), and the egg comes when it comes.
// ======================================================================================================
export const hensTree = (h = {}) => ({
  id: "hens",
  start: (g) => (is(g, "nevada.jolene") ? "after" : "step"),
  nodes: {
    step: {
      options: [
        { id: "attention", line: "nevada.hens.opt.attention", once: true, say: ["nevada.hens.attention.2"] },   // the General's method: not hers to order
        { id: "hello", line: "nevada.hens.opt.hello", once: true, say: ["nevada.hens.hello.2"] },               // the clue: they are looking at something
        { id: "cluck", line: "nevada.hens.opt.cluck", once: true, say: ["nevada.hens.cluck.2"] },               // the laugh
        { id: "look", line: "nevada.hens.opt.look", do: h.row, then: "guarding" },                              // the way
        { id: "stepBye", line: "nevada.hens.opt.bye", then: "exit" },
      ],
    },
    guarding: {
      say: ["nevada.hens.look.1", "nevada.hens.look.2", "nevada.hens.look.3", "nevada.hens.look.4"],
      options: [
        { id: "salute", line: "nevada.hens.opt.salute", once: true, say: ["nevada.hens.salute.2"] },
        { id: "tell", line: "nevada.hens.opt.tell", then: "tell1" },
      ],
    },
    tell1: { say: ["nevada.hens.tell.1"], then: async (g) => { if (h.sit) await h.sit(g, 1); return "tell2"; } },
    tell2: { say: ["nevada.hens.tell.2"], then: async (g) => { if (h.sit) await h.sit(g, 2); return "tell3"; } },
    tell3: { say: ["nevada.hens.tell.3"], then: async (g) => { if (h.egg) await h.egg(g); return "egg"; } },
    egg: {
      say: ["nevada.hens.egg.1", "nevada.hens.jolene.1", "nevada.hens.jolene.2", "nevada.hens.jolene.3"],
      then: async (g) => { if (h.giveEgg) await h.giveEgg(g); g.flag("nevada.jolene", true); return "egg2"; },
    },
    egg2: { say: ["nevada.hens.egg.2"], then: "exit" },
    after: { say: ["nevada.hens.after"], then: "exit" },
  },
});

// ======================================================================================================
// letterboxTree: the Son, through the coin door: g.talk(letterboxTree(h), { through: "son" }). Through a door the menus
// are his words (the engine's way): the options are the Son's lines, and the family answer on stage.
// LETTER-17 (round seventeen): the night Mom hears her son, rewritten as the author asked (16 October; the design is
// briefs/out/office-hq-design.md, section 2). Is that YOU; Mom, on her knees at the door, and every rule of her voice gone
// at once; he explains as best he can (the player picks what he tries next, and each try moves her a step from Italy to
// 44 B.C.), and once three of the year's clues are in (CLUES, as they were) he tells her it is B.C. and Big Sister pins it;
// Mom, slowly; she comes back ("Have you eaten?"); the rest of the talk, with a mother's questions in it, and the penny
// for luck; his warning, which the first time ends the talk (nevada.heardSon: the beat), and her answer; and Grandpa Joe,
// who heard all of it, and Ranger with her handbag. A first talk broken off (a game saved in the middle of it) picks up
// where it was, after "You're BACK!". Every time after, the rest of the talk, and goodbye.
// ======================================================================================================
const CLUES = ["smell", "chickens", "caesar", "togas", "temple"];
const cluesHeard = (g) => CLUES.filter((c) => g.asked("letterbox/" + c) > 0).length;

export const letterboxTree = (h = {}) => {
  let going = null;                                           // Mom on her way to the door (h.kneel), while the two of them say hello
  return {
    id: "letterbox",
    start: (g) => {
      if (is(g, "nevada.heardSon") || is(g, "nevada.sonMet")) return "again";
      return "hail." + (["mom", "bigsis", "lilsis"].includes(who(g)) ? who(g) : "lilsis");
    },
    nodes: {
      "hail.mom": { say: ["nevada.letterbox.hail.mom"], then: "voice" },
      "hail.bigsis": { say: ["nevada.letterbox.hail.bigsis"], then: "voice" },
      "hail.lilsis": { say: ["nevada.letterbox.hail.lilsis"], then: "voice" },
      // his voice; the handbag goes down, and Mom comes to the door (h.kneel), while he and his little sister say hello
      voice: { say: ["nevada.letterbox.son.0"], then: (g) => { going = h.kneel ? h.kneel(g) : null; return "hello"; } },
      hello: {
        say: ["nevada.letterbox.lilsis.1", "nevada.letterbox.son.1", "nevada.letterbox.lilsis.2", "nevada.letterbox.son.2"],
        then: async () => { if (going) await going; going = null; return "mom"; },
      },
      // Mom; and the girls, very quietly
      mom: {
        say: ["nevada.letterbox.mom.1", "nevada.letterbox.son.3", "nevada.letterbox.mom.2", "nevada.letterbox.bigsis.1", "nevada.letterbox.lilsis.3"],
        then: (g) => { g.flag("nevada.sonMet", true); return "explain"; },
      },
      // he explains, as best he can: each try once, in any order ("not THAT Rome" once he has said Rome)
      explain: {
        options: [
          { id: "where", line: "nevada.letterbox.opt.where", once: true, say: ["nevada.letterbox.mom.italy"] },
          { id: "old", line: "nevada.letterbox.opt.old", once: true, when: (g) => g.asked("letterbox/where") > 0, say: ["nevada.letterbox.mom.funny", "nevada.letterbox.son.funny"] },
          { id: "smell", line: "nevada.letterbox.opt.smell", once: true, say: ["nevada.letterbox.big.smell", "nevada.letterbox.mom.smell"] },
          { id: "chickens", line: "nevada.letterbox.opt.chickens", once: true, say: ["nevada.letterbox.lil.chickens", "nevada.letterbox.mom.chickens"] },
          { id: "caesar", line: "nevada.letterbox.opt.caesar", once: true, say: ["nevada.letterbox.mom.caesar", "nevada.letterbox.big.caesar"] },
          { id: "togas", line: "nevada.letterbox.opt.togas", once: true, say: ["nevada.letterbox.big.togas", "nevada.letterbox.mom.grownup", "nevada.letterbox.son.counting"] },
          { id: "temple", line: "nevada.letterbox.opt.temple", once: true, say: ["nevada.letterbox.mom.temple", "nevada.letterbox.son.temple"] },
          // with three of the clues in: it is B.C., Big Sister pins the year, and Mom understands. She sits back on her
          // heels, and the girls come and stand either side of her (h.heels).
          { id: "pin", line: "nevada.letterbox.opt.when", when: (g) => cluesHeard(g) >= 3,
            say: ["nevada.letterbox.mom.before", "nevada.letterbox.big.pin.1", "nevada.letterbox.big.pin.2", "nevada.letterbox.mom.then"], set: "nevada.sonPinned", do: h.heels, then: "okay" },
        ],
      },
      okay: { say: ["nevada.letterbox.son.confirm"], then: async (g) => { if (h.lean) await h.lean(g); return "eaten"; } },
      // she comes back: the next thing she can fix
      eaten: {
        say: ["nevada.letterbox.mom.eaten"],
        options: [
          { id: "rome", line: "nevada.letterbox.opt.rome", say: ["nevada.letterbox.mom.first"] },
          { id: "ate", line: "nevada.letterbox.opt.ate", say: ["nevada.letterbox.mom.ate"], then: "after" },
        ],
      },
      // the rest of the talk, and a mother's questions in it (warm enough, where he sleeps, who is kind to him)
      after: {
        options: [
          { id: "send", line: "nevada.letterbox.opt.send", when: (g) => g.has("penny") && !is(g, "nevada.pennySent"), say: ["nevada.letterbox.penny.lil"], do: h.penny, then: "sent" },
          { id: "sendLater", line: "nevada.letterbox.opt.send", when: (g) => !g.has("penny") && is(g, "nevada.pennies") && !is(g, "nevada.pennySent"), say: ["nevada.letterbox.penny.mine"] },
          { id: "sendNone", line: "nevada.letterbox.opt.send", when: (g) => !is(g, "nevada.pennies") && !is(g, "nevada.pennySent"), say: ["nevada.letterbox.penny.none"] },
          { id: "keys", line: "nevada.letterbox.opt.keys", say: ["nevada.letterbox.mom.keys"] },
          { id: "warm", line: "nevada.letterbox.opt.warm", say: ["nevada.letterbox.mom.warm", "nevada.letterbox.son.warm"] },
          { id: "sleep", line: "nevada.letterbox.opt.sleep", say: ["nevada.letterbox.mom.sleep", "nevada.letterbox.son.sleep", "nevada.letterbox.mom.sleep.2"] },
          { id: "kind", line: "nevada.letterbox.opt.kind", say: ["nevada.letterbox.mom.kind", "nevada.letterbox.son.kind", "nevada.letterbox.mom.kind.2"] },
          { id: "there", line: "nevada.letterbox.opt.there", say: ["nevada.letterbox.lil.there", "nevada.letterbox.son.phone", "nevada.letterbox.big.phone", "nevada.letterbox.son.quarter"] },
          { id: "dog", line: "nevada.letterbox.opt.dog", say: ["nevada.letterbox.lil.dog", "nevada.letterbox.son.dog"] },
          // the first time, what he has to tell her, which ends the talk; every time after, goodbye
          { id: "warn", line: "nevada.letterbox.son.warn.0", when: (g) => !is(g, "nevada.heardSon"), then: "warning" },
          { id: "sonBye", line: "nevada.letterbox.opt.bye", when: (g) => is(g, "nevada.heardSon"), say: ["nevada.letterbox.mom.bye", "nevada.letterbox.lil.bye", "nevada.letterbox.son.bye"], then: "exit" },
        ],
      },
      sent: {
        say: ["nevada.letterbox.penny.son", "nevada.letterbox.penny.lil.2", "nevada.letterbox.chicken.lil", "nevada.letterbox.chicken.big", "nevada.letterbox.chicken.son"],
        then: "back",
      },
      // his warning, and her answer: she does not promise
      warning: {
        say: ["nevada.letterbox.son.warn", "nevada.letterbox.mom.heard", "nevada.letterbox.big.no", "nevada.letterbox.mom.find", "nevada.letterbox.lil.coming", "nevada.letterbox.son.snacks",
          "nevada.letterbox.mom.love", "nevada.letterbox.son.love", "nevada.letterbox.big.noted", "nevada.letterbox.lil.bye", "nevada.letterbox.son.bye"],
        then: async (g) => { g.flag("nevada.heardSon", true); if (h.rise) await h.rise(g); return "joe"; },
      },
      // Grandpa Joe, who heard all of it; and Ranger brings her the handbag (Ranger's "...", and Grandpa Joe says what he means)
      joe: { say: ["nevada.letterbox.joe.1"], then: async (g) => { if (h.turn) await h.turn(g); return "joe2"; } },
      joe2: { say: ["nevada.letterbox.joe.2", "nevada.letterbox.mom.he", "nevada.letterbox.joe.3"], then: async (g) => { if (h.bring) await h.bring(g); return "bag"; } },
      bag: { say: ["nevada.ranger.dots", "nevada.letterbox.joe.bag"], then: async (g) => { if (h.take) await h.take(g); return "thanks"; } },
      thanks: { say: ["nevada.letterbox.mom.ranger"], then: "exit" },
      // spoken into again; or a first talk broken off, picked up where it was
      again: {
        say: ["nevada.letterbox.son.again"],
        then: (g) => (is(g, "nevada.heardSon") || g.asked("letterbox/ate") > 0 ? "after" : is(g, "nevada.sonPinned") ? "eaten" : "explain"),
      },
    },
  };
};

// ======================================================================================================
// dividerTree: Act Five. Grandpa Joe, to the suits through the divider while it is down. Talk does not put it up
// ("Sir, we are required to maintain visual."); singing does, and that is #14's lever.
// ======================================================================================================
export const dividerTree = (h = {}) => ({
  id: "divider",
  start: "sir",
  nodes: {
    sir: { say: ["limo.divider.sir"], then: "talk" },
    talk: {
      options: [
        { id: "where", line: "limo.divider.opt.where", say: { 1: ["limo.open.2", "limo.divider.where.joe", "limo.open.4"], more: ["limo.open.2"] } },
        { id: "office", line: "limo.divider.opt.office", say: { 1: ["limo.divider.office.1", "limo.divider.office.2", "limo.divider.office.3", "limo.divider.office.4"], more: ["limo.divider.office.3"] } },
        { id: "what", line: "limo.divider.opt.what", say: ["limo.divider.what.1", "limo.divider.what.2", "limo.open.4"] },
        { id: "regs", line: "limo.divider.opt.regs", say: { 1: ["limo.divider.regs.1", "limo.divider.regs.2", "limo.divider.regs.3"], 2: ["limo.divider.regs.4"], more: ["limo.divider.regs.5"] } },
        { id: "burger", line: "limo.divider.opt.burger", say: ["limo.divider.burger.1", "limo.divider.burger.jed"] },
        { id: "up", line: "limo.divider.opt.up", say: ["limo.ropes.visual"] },
        // the lever: the Last Stop Rag, hummed (his own tune: no words)
        { id: "music", line: "limo.ropes.music", say: { 1: ["limo.ropes.required", "limo.sing.1"], 2: ["limo.ropes.required.2", "limo.sing.2"], more: ["limo.ropes.required.3", "limo.sing.3"] },
          do: h.sing, then: (g) => (g.asked("divider/music") === 1 ? "singing" : "singing2") },
        { id: "dividerBye", line: "limo.divider.opt.bye", say: ["limo.divider.bye"], then: "exit" },
      ],
    },
    singing: { say: ["limo.ropes.stop", "limo.ropes.medical"], then: "exit" },
    singing2: { say: ["limo.ropes.stop.2", "limo.ropes.medical.2"], then: "exit" },
  },
});

/** Every tree, by name, for the tests. */
export const trees = { joeTree, joleneTree, rangerTree, hensTree, letterboxTree, dividerTree };

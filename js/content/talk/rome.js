// The talks of the bigger Rome (Act Two, round thirteen: ROME-13W, new; briefs/ROME-13.md and WRITE-13R.md), as
// dialogue trees. Plain data in the engine's format (docs/DESIGN.md, section 7, "Dialogue trees"): every word is a line
// id (js/content/lines/rome.en.js). An option's `line` is the Son's, said when he picks it; its `say` is the reply (a
// list, or { 1, 2, more } by how many times it has been picked); `set` makes facts true; `do` is a script (it runs after
// the reply); `then` goes to a node, "back", "root" or "exit" (or is a function of the game giving one).
//
// Each tree is a function of a `hooks` object, so that the scene hands in the scripts a branch needs:
//     import { gaulTree, phyllisTree } from "../talk/rome.js";
//     const GAUL = gaulTree({ point, bow, swap, leave });
//     ...  use: (g) => g.talk(GAUL)
// A hook that is not handed in is passed over: the talk still says every line and sets every fact of its own. The
// facts that go with a thing changing hands (rome.swapped, rome.hasLamp, rome.felixWord, rome.wishGranted) are the hooks'
// to set, because they go with the thing (the hook that hands it over sets them). None of the hooks may say a line the
// tree says; the one hook that says lines of its own (anser's `stomp`) has them listed here.
//
// THE HOOKS, and what each must do.
//   gaulTree (the Gaul, at the hoarding of the new senate house's site: the Forum)
//     point(g)      he turns to the site and points at the hole where the House was. Staging only (runs before his line
//                   "There is the senate house.").
//     bow(g)        he bows, after "Then you are a true Roman. Thank you." Staging only.
//     swap(g)       he walks to the hoarding's gateway, through it to `behind`, where its cut-out hides him; he becomes
//                   `gaul-own`; a beat; he walks back to his mark in his own toga. Must take "gaultoga", give "toga", and
//                   set rome.swapped.
//     leave(g)      he goes off up the square toward the plain, and out of the picture. Staging only (the scene keeps
//                   him off the Forum from then on, by rome.swapped).
//   phyllisTree (Phyllis, on her stool among her baskets at the foot of Castor's temple: the Forum)
//     stand(g)      she stands, hangs a garland on her pole, comes back and sits. Staging only.
//     lamp(g)       she unwraps the lamp from her lap and holds it out; the boy takes it (g.reach()). Must give "lamp", set
//                   rome.hasLamp, and make her `phyllis-free`.
//     grant(g)      her leave: she closes the boy's hand over the coin (or nods). Must set rome.wishGranted.
//   titusTree (Titus, on top of the middle statue base among the kings: the Capitol)
//     feet(g)       he puts a foot down, every goose stretches its neck and hisses (the flock's pose("look", 1.2), the
//                   sound goosehiss), and he draws his feet up again. Staging only.
//   anserTree (Titus Rubrius Anser, by the geese's pen: the Capitol)
//     shake(g)      he shakes his basket of grain. Staging only.
//     stomp(g)      the solution of Juno's Geese, the same script as a click on the geese once rome.knowsGeese is true. In
//                   order: the boy walks to `atbase` and faces N; he says rome.geese.stomp; his sneakers flash red twice;
//                   the geese shriek, flap and run for their pen (herd), and rome.geeseGone; Titus hops down and says
//                   rome.titus.down; he holds out the breakfast and says rome.titus.give; the boy takes it (g.give
//                   "breakfast", rome.hasBreakfast, and rome.knowsBoy and rome.metTitus if not yet set); rome.titus.give.son;
//                   Titus becomes `titus-free`, says rome.titus.run and runs off down the hill; then the goose-keeper says
//                   rome.anser.last. (The tree ends the talk after it.)
//   eleazarTree (Eleazar, on his bench before the house of prayer, after he has come down from his window: across the
//   Tiber; the scene drops the music for the whole talk). Every hook here is staging only, slow, with room round the words.
//     aside(g, on)  on: the boy turns away from the old man, to us, for a line that is not for him; off: he turns back.
//     pray(g)       the old man stands (sit(false)), walks to `pray_eleazar` and faces W, toward the river and Jerusalem;
//                   the boy walks to `pray_son` and faces W; both pray (pray(true): the boy's head goes down, his hair
//                   stays up). The tree then says the prayer.
//     amen(g)       both stop praying (pray(false)).
//     bless(g)      the old man faces E; the boy stands facing him (W), on the same row, his feet BLESS_STEP of the old
//                   man's height in front of the old man's; the old man's hand on the boy's head (his `bless` hold), the
//                   boy's head going down. The tree then says Numbers 6:25.
//     release(g)    the hand comes away; both heads come up.
//     rest(g)       the old man goes back to his bench and sits.
//     away(g)       the boy walks a few steps off along the lane and turns to us (his last line is to us).
//   mariamTree (Mariam, in the hen yard behind its fence, talked to from the lane)
//     crouch(g)     she crouches to look a hen in the eye, and stands again. Staging only.
//     aside(g, on)  as eleazarTree's: the boy turns to us for his line at the hens, and back.
//   felixTree (Felix, between the landing and the barge)
//     setDown(g)    he sets his bale down (`felix-free`). Staging only (the scene has him take it up again after the talk).
//     lamp(g)       the boy holds out the lamp and Felix takes it. Must take "lamp" and set rome.felixWord.
//     aside(g, on)  as eleazarTree's: the boy turns to us for his line at "Corinth", and back.
//
// THE FACTS the `when`s and `start`s read (the writer's ids.md for the round says who sets each). Set by the trees
// themselves: rome.metGaul, rome.gaulAnswered, rome.metPhyllis, rome.metTitus, rome.knowsBoy (Titus says whose boy he is),
// rome.metAnser, rome.knowsGeese, rome.metEleazar, rome.prayed, rome.blessed, rome.metMariam, rome.sawHens, rome.metFelix.
// Set by the hooks: rome.swapped, rome.hasLamp, rome.felixWord, rome.wishGranted, rome.geeseGone, rome.hasBreakfast. Set
// by the scenes: rome.knowsSenate, rome.knowsWish, rome.sawCapitol, rome.sawTheater, rome.eleazarDown, rome.metDateSeller
// (as now). And g.has("gaultoga"), g.has("coin"), g.has("quarter"), g.has("lamp") (the Son is carrying it), and
// g.asked("<tree>/<option>"). One test reads the engine's own count of lines said (g.store.data.seenLines), as the
// street's script does, because the date seller's blessing sets no fact of its own: whether rome.dateseller.bless.2 has
// been said (Eleazar's "PIECES").
//
// What nobody here says (the design's 5.9 and 6.1): nobody knows what will happen in Pompey's hall today; the Gaul goes to
// an ordinary meeting. Eleazar never names Jesus, never says when, never says the promised one is God, says nothing
// against anybody's gods, argues with nobody; the Son never tells him what is coming. Scripture is quoted three times
// here, King James Version, exact (Isaiah 40:31 to its semicolon, Numbers 6:25, Numbers 6:26), each reference said by the
// Son; everything else from the Bible is told in the speaker's own words. (PASS-17R: since the author's rule of 16 October
// no reference is said aloud: the Son says where he knows the words from; the references are in docs/CHARACTERS.md.)

const is = (g, fact) => !!g.flag(fact);
/** The engine's count of the lines it has said (kept in the save), as the street's own script reads it. */
const heard = (g, id) => !!(g.store && g.store.data && g.store.data.seenLines && g.store.data.seenLines[id]);
/** Run a hook if the scene handed it in. */
const run = async (hook, g, ...args) => { if (hook) await hook(g, ...args); };

// ======================================================================================================
// gaulTree: the Gaul (NEW 2, Nobody Will Show Him). He tells the joke on himself before anybody else can, and asks his
// question; the answers are the options, the right one ("In Pompey's hall") on offer once the boy has heard it. The
// togas, once he has the Gaul's toga AND has answered, in either order; then his going. He can be met before the boy has
// the toga: he asks, is answered, thanks him, and the swap waits.
// ======================================================================================================
export const gaulTree = (h = {}) => ({
  id: "gaul",
  start: (g) => (is(g, "rome.gaulAnswered") ? "answeredAgain" : is(g, "rome.metGaul") ? "again" : "meet"),
  nodes: {
    // ---- He is at the hoarding, tugging the short toga down. Four ways in: the way in, the laugh (and a plant: the
    // toga is not his, and he does not know it), the Son getting Rome wrong out loud, and the wrong foot.
    meet: {
      options: [
        { id: "hi", line: "rome.gaul.opt.hi", say: ["rome.gaul.hi"], set: "rome.metGaul", then: "who" },
        { id: "short", line: "rome.gaul.opt.short", say: ["rome.gaul.short.1", "rome.gaul.short.2"], set: "rome.metGaul", then: "who" },
        { id: "viking", line: "rome.gaul.opt.viking", say: ["rome.gaul.viking"], set: "rome.metGaul", then: "who" },
        { id: "way", line: "rome.gaul.opt.way", say: ["rome.gaul.way"], set: "rome.metGaul", then: "who" },
      ],
    },
    // who he is, why nobody answers him (his own words: "It is a joke. I am it."), where he went, and his question
    who: { say: ["rome.gaul.who.1", "rome.gaul.who.son", "rome.gaul.who.2", "rome.gaul.who.3", "rome.gaul.who.4", "rome.gaul.who.5", "rome.gaul.who.6"], then: "ask" },
    again: { say: ["rome.gaul.again"], then: "ask" },
    // ---- his question: where does the Senate meet today? The answers, and the rest.
    ask: {
      options: [
        { id: "house", line: "rome.gaul.opt.house", do: h.point, then: (g) => (g.asked("gaul/house") === 1 ? "hole" : "hole2") },
        { id: "capitol", line: "rome.gaul.opt.capitol", when: (g) => !is(g, "rome.sawCapitol"), say: { 1: ["rome.gaul.capitol.1", "rome.gaul.capitol.2"], more: ["rome.gaul.capitol.3"] } },
        { id: "geese", line: "rome.gaul.opt.geese", when: (g) => is(g, "rome.sawCapitol"), say: { 1: ["rome.gaul.geese.1"], more: ["rome.gaul.geese.2"] } },
        { id: "caesar", line: "rome.gaul.opt.caesar", say: { 1: ["rome.gaul.caesar.1", "rome.gaul.caesar.son"], more: ["rome.gaul.caesar.2"] } },
        { id: "dunno", line: "rome.gaul.opt.dunno", say: { 1: ["rome.gaul.dunno.1"], 2: ["rome.gaul.dunno.2"], more: ["rome.gaul.dunno.3"] }, do: h.bow },
        // the answer, heard from the senator (his speech) or from Walnut
        { id: "pompey", line: "rome.gaul.opt.pompey", when: (g) => is(g, "rome.knowsSenate"), say: ["rome.gaul.pompey"], set: "rome.gaulAnswered",
          then: (g) => (is(g, "rome.sawTheater") ? "saw" : "heard") },
        // the laugh: Rome's song about Gauls, told by the Gaul, wryly (the verses are never quoted)
        { id: "song", line: "rome.gaul.opt.song", say: { 1: ["rome.gaul.song.1", "rome.gaul.song.2", "rome.gaul.song.son", "rome.gaul.song.3"], more: ["rome.gaul.song.4"] } },
        { id: "mustache", line: "rome.gaul.opt.mustache", once: true, say: ["rome.gaul.mustache.1", "rome.gaul.mustache.son", "rome.gaul.mustache.2"] },
        // the toga held out before he has his answer: first the Senate, then his knees
        { id: "togaFirst", clue: true, line: "rome.gaul.opt.swap", when: (g) => g.has("gaultoga"), say: { 1: ["rome.gaul.swap.first"], more: ["rome.gaul.swap.first.2"] } },
        { id: "bye", line: "rome.gaul.opt.bye", say: { 1: ["rome.gaul.bye.1"], more: ["rome.gaul.bye.2"] }, then: "exit" },
      ],
    },
    hole: { say: ["rome.gaul.house.1", "rome.gaul.house.son"], then: "back" },
    hole2: { say: ["rome.gaul.house.2"], then: "back" },
    saw: { say: ["rome.gaul.saw.son", "rome.gaul.saw"], then: "answered" },
    heard: { say: ["rome.gaul.heard.son", "rome.gaul.heard"], then: "answered" },
    answered: { say: ["rome.gaul.answered.1", "rome.gaul.answered.2"], then: "waiting" },
    answeredAgain: { say: ["rome.gaul.welcome"], then: "waiting" },
    // ---- he knows the way; he will not go with his knees out. The swap, once the boy has the Gaul's toga.
    waiting: {
      options: [
        { id: "swap", line: "rome.gaul.opt.swap", when: (g) => g.has("gaultoga"), say: ["rome.gaul.swap.1"], do: h.swap, then: "swapped" },
        { id: "why", clue: true, line: "rome.gaul.opt.why", when: (g) => !g.has("gaultoga"), say: { 1: ["rome.gaul.why.1", "rome.gaul.why.2"], more: ["rome.gaul.why.3"] } },
        { id: "remind", line: "rome.gaul.opt.remind", say: { 1: ["rome.gaul.remind.1"], more: ["rome.gaul.remind.2"] } },
        { id: "songAfter", line: "rome.gaul.opt.song", when: (g) => !g.asked("gaul/song"), once: true, say: ["rome.gaul.song.1", "rome.gaul.song.2", "rome.gaul.song.son", "rome.gaul.song.3"] },
        { id: "mustacheAfter", line: "rome.gaul.opt.mustache", when: (g) => !g.asked("gaul/mustache"), once: true, say: ["rome.gaul.mustache.1", "rome.gaul.mustache.son", "rome.gaul.mustache.2"] },
        { id: "byeWaiting", line: "rome.gaul.opt.byewait", say: { 1: ["rome.gaul.byewait.1"], more: ["rome.gaul.byewait.2"] }, then: "exit" },
      ],
    },
    // after the swap (the hook has changed him and the togas): his going
    swapped: {
      say: ["rome.gaul.swap.2", "rome.gaul.swap.son", "rome.gaul.leave.1", "rome.gaul.leave.son", "rome.gaul.leave.2"],
      then: async (g) => { await run(h.leave, g); return "exit"; },
    },
  },
});

// ======================================================================================================
// phyllisTree: Phyllis (NEW 4, Interest Is Extra Wishes: her side). Her patter; Anna Perenna's feast (why she cannot
// leave her baskets); her son and Corinth; the Twins' temple she sits under; then, when the boy has the coin and knows
// whose it was, the wish, the wrong tries and the lamp; and, when Felix has given his word, her leave.
// ======================================================================================================
export const phyllisTree = (h = {}) => ({
  id: "phyllis",
  start: (g) => {
    if (is(g, "rome.wishGranted")) return "done";
    if (is(g, "rome.felixWord")) return "word";
    if (is(g, "rome.hasLamp")) return "waiting";
    return is(g, "rome.metPhyllis") ? "again" : "cry";
  },
  nodes: {
    cry: { say: ["rome.phyllis.cry"], then: (g) => { g.flag("rome.metPhyllis", true); return "open"; } },
    again: { say: ["rome.phyllis.again"], then: "open" },
    open: {
      options: [
        { id: "anna", line: "rome.phyllis.opt.anna", say: { 1: ["rome.phyllis.anna.1", "rome.phyllis.anna.2"], more: ["rome.phyllis.anna.3"] }, do: h.stand },     // the clue: she cannot leave
        { id: "sweetheart", line: "rome.phyllis.opt.sweetheart", once: true, say: ["rome.phyllis.sweetheart.1", "rome.phyllis.sweetheart.son", "rome.phyllis.sweetheart.2"] },    // the laugh
        { id: "son", clue: true, line: "rome.phyllis.opt.son", say: { 1: ["rome.phyllis.son.1", "rome.phyllis.son.2", "rome.phyllis.son.3", "rome.phyllis.son.son"], more: ["rome.phyllis.son.4"] } },
        { id: "twins", line: "rome.phyllis.opt.twins", once: true, say: ["rome.phyllis.twins.1", "rome.phyllis.twins.2", "rome.phyllis.twins.son"] },
        // the lever: the coin, and whose it was (Walnut has said so)
        { id: "wish", clue: true, line: "rome.phyllis.opt.wish", when: (g) => g.has("coin") && is(g, "rome.knowsWish") && !is(g, "rome.hasLamp"),
          say: { 1: ["rome.phyllis.wish.1", "rome.phyllis.wish.2", "rome.phyllis.wish.3", "rome.phyllis.wish.4"], more: ["rome.phyllis.wish.again"] }, then: "wish" },
        { id: "bye", line: "rome.phyllis.opt.bye", say: { 1: ["rome.phyllis.bye.1"], more: ["rome.phyllis.bye.2"] }, then: "exit" },
      ],
    },
    // the wish told: give it back (no), pay for it (no), or take the lamp to her son
    wish: {
      options: [
        { id: "giveBack", clue: true, line: "rome.phyllis.opt.giveback", say: { 1: ["rome.phyllis.giveback"], more: ["rome.phyllis.giveback.2"] } },
        { id: "quarter", line: "rome.phyllis.opt.quarter", when: (g) => g.has("quarter"), say: { 1: ["rome.phyllis.quarter"], more: ["rome.phyllis.quarter.2"] } },
        { id: "take", line: "rome.phyllis.opt.take", say: ["rome.phyllis.take.1", "rome.phyllis.take.2"], do: h.lamp, then: "lamped" },
        { id: "think", line: "rome.phyllis.opt.think", say: ["rome.phyllis.think"], then: "exit" },
      ],
    },
    lamped: { say: ["rome.phyllis.lamped"], then: "exit" },
    // the lamp is on its way
    waiting: {
      say: ["rome.phyllis.waiting"],
      options: [
        { id: "where", clue: true, line: "rome.phyllis.opt.where", say: { 1: ["rome.phyllis.where.1"], more: ["rome.phyllis.where.2"] } },
        { id: "lampBack", clue: true, line: "rome.phyllis.opt.lampback", say: ["rome.phyllis.lampback"] },
        { id: "byeWaiting", line: "rome.phyllis.opt.byewait", say: ["rome.phyllis.byewait"], then: "exit" },
      ],
    },
    // Felix has given his word: the boy brings it back
    word: {
      say: ["rome.phyllis.word"],
      options: [
        { id: "news", line: "rome.phyllis.opt.news", say: ["rome.phyllis.news.1", "rome.phyllis.news.2", "rome.phyllis.news.3"], do: h.grant, then: "granted" },
        { id: "guess", line: "rome.phyllis.opt.guess", once: true, say: ["rome.phyllis.guess"] },
      ],
    },
    granted: { say: ["rome.phyllis.granted.son"], then: "exit" },
    done: { say: ["rome.phyllis.done"], then: "open" },
  },
});

// ======================================================================================================
// titusTree: Titus, the keeper's boy, on top of a statue base among the kings, the soothsayer's breakfast in his lap, the
// sacred geese round its foot (NEW 3, Juno's Geese). Stuck, and saying he is not. If the boy has come up before the keeper
// told him anything, Titus says whose boy he is and whose breakfast it is (rome.knowsBoy).
// ======================================================================================================
export const titusTree = (h = {}) => ({
  id: "titus",
  start: (g) => (is(g, "rome.metTitus") ? "again" : "meet"),
  nodes: {
    meet: {
      options: [
        { id: "sent", line: "rome.titus.opt.sent", when: (g) => is(g, "rome.knowsBoy"), say: ["rome.titus.sent"], set: ["rome.metTitus", "rome.knowsBoy"], then: "who" },     // his father's errand
        { id: "stuck", line: "rome.titus.opt.stuck", say: ["rome.titus.stuck.1", "rome.titus.stuck.2"], set: ["rome.metTitus", "rome.knowsBoy"], then: "who" },
        { id: "statue", line: "rome.titus.opt.statue", say: ["rome.titus.statue"], set: ["rome.metTitus", "rome.knowsBoy"], then: "who" },
        { id: "sausage", line: "rome.titus.opt.sausage", say: ["rome.titus.sausage"], set: ["rome.metTitus", "rome.knowsBoy"], then: "who" },
        { id: "jump", line: "rome.titus.opt.jump", say: ["rome.titus.jump.1"], set: ["rome.metTitus", "rome.knowsBoy"], then: "who" },
      ],
    },
    who: { say: ["rome.titus.who.1", "rome.titus.who.2", "rome.titus.who.3"], then: "ask" },
    again: { say: ["rome.titus.again"], then: "ask" },
    ask: {
      options: [
        // what the geese do whenever he puts a foot down (hook feet), and the second time, what he will say about it
        { id: "geese", clue: true, line: "rome.titus.opt.geese", say: { 1: ["rome.titus.geese.1"], more: ["rome.titus.geese.again"] }, do: h.feet,
          then: (g) => (g.asked("titus/geese") === 1 ? "feet" : null) },
        { id: "ewe", line: "rome.titus.opt.ewe", once: true, say: ["rome.titus.ewe.1", "rome.titus.ewe.2", "rome.titus.ewe.son"] },
        { id: "father", line: "rome.titus.opt.father", say: { 1: ["rome.titus.father.1", "rome.titus.father.2"], more: ["rome.titus.father.3"] } },
        { id: "jump2", line: "rome.titus.opt.jump2", say: { 1: ["rome.titus.jump.2"], more: ["rome.titus.jump.3"] } },
        { id: "help", clue: true, line: "rome.titus.opt.help", say: { 1: ["rome.titus.help.1", "rome.titus.help.2"], more: ["rome.titus.help.3"] } },     // the clue: ask old Anser
        { id: "bye", line: "rome.titus.opt.bye", say: { 1: ["rome.titus.bye.1"], more: ["rome.titus.bye.2"] }, then: "exit" },
      ],
    },
    feet: { say: ["rome.titus.geese.2"], then: "back" },
  },
});

// ======================================================================================================
// anserTree: Titus Rubrius Anser, who feeds the sacred geese (NEW 3's clue). His geese, which the Republic feeds; the
// dogs that guard the hill at night; his name; Juno's other temple, Moneta; and the tale, told as he would tell it, long
// ago and with no year: it is the instructions. After the tale, the lever: the boy puts it to the test (hook stomp).
// ======================================================================================================
const TALE = ["rome.anser.tale.1", "rome.anser.tale.2", "rome.anser.tale.3", "rome.anser.tale.4", "rome.anser.tale.5", "rome.anser.tale.6", "rome.anser.tale.son"];
export const anserTree = (h = {}) => ({
  id: "anser",
  start: (g) => (is(g, "rome.geeseGone") ? "after" : is(g, "rome.metAnser") ? "again" : "meet"),
  nodes: {
    // ---- four ways in; every one of his answers mentions the night the geese saved the city (he cannot help it)
    meet: {
      options: [
        { id: "move", line: "rome.anser.opt.move", say: ["rome.anser.move.1", "rome.anser.move.2"], set: "rome.metAnser", do: h.shake, then: "ask" },
        { id: "chickens", line: "rome.anser.opt.chickens", say: ["rome.anser.chickens.1", "rome.anser.chickens.2"], set: "rome.metAnser", then: "ask" },
        { id: "name", line: "rome.anser.opt.name", say: ["rome.anser.name.1", "rome.anser.name.2", "rome.anser.name.son", "rome.anser.name.3"], set: "rome.metAnser", then: "ask" },
        { id: "feed", line: "rome.anser.opt.feed", say: ["rome.anser.feed.1", "rome.anser.feed.2"], set: "rome.metAnser", do: h.shake, then: "ask" },
      ],
    },
    again: { say: ["rome.anser.again"], then: "ask" },
    ask: {
      options: [
        // the clue: the tale (the second time he tells it gladly again; the third time is a running gag)
        { id: "saved", clue: true, line: "rome.anser.opt.saved", say: { 1: TALE, 2: ["rome.anser.tale.again.1", "rome.anser.tale.again.son", "rome.anser.tale.again.2"], more: ["rome.anser.tale.more", "rome.anser.tale.more.son"] },
          set: "rome.knowsGeese" },
        // the lever: once he has told it, the boy puts it to the test (the hook says the lines of the stomp)
        { id: "test", line: "rome.anser.opt.test", when: (g) => is(g, "rome.knowsGeese") && !is(g, "rome.geeseGone"), do: h.stomp, then: "exit" },
        { id: "moveAsk", line: "rome.anser.opt.move2", say: { 1: ["rome.anser.move.3"], 2: ["rome.anser.move.4"], more: ["rome.anser.move.5"] }, do: h.shake },
        { id: "dogs", line: "rome.anser.opt.dogs", say: { 1: ["rome.anser.dogs.1", "rome.anser.dogs.2"], more: ["rome.anser.dogs.3"] } },
        { id: "moneta", line: "rome.anser.opt.moneta", say: { 1: ["rome.anser.moneta.1", "rome.anser.moneta.son", "rome.anser.moneta.2"], more: ["rome.anser.moneta.3"] } },
        { id: "nameAsk", line: "rome.anser.opt.name", when: (g) => !g.asked("anser/name"), once: true, say: ["rome.anser.name.1", "rome.anser.name.2", "rome.anser.name.son", "rome.anser.name.3"] },
        { id: "bye", line: "rome.anser.opt.bye", say: { 1: ["rome.anser.bye.1"], more: ["rome.anser.bye.2"] }, then: "exit" },
      ],
    },
    // ---- after the stomp: the geese in their pen, and the goose-keeper not quite recovered
    after: {
      say: ["rome.anser.after"],
      options: [
        { id: "moneta2", line: "rome.anser.opt.moneta", say: { 1: ["rome.anser.moneta.1", "rome.anser.moneta.son", "rome.anser.moneta.2"], more: ["rome.anser.moneta.3"] } },
        { id: "sorry", line: "rome.anser.opt.sorry", once: true, say: ["rome.anser.sorry"] },
        { id: "byeAfter", line: "rome.anser.opt.bye", say: ["rome.anser.bye.after"], then: "exit" },
      ],
    },
  },
});

// ======================================================================================================
// eleazarTree: Eleazar, the devout Jew, the date seller's father-in-law, on his bench once he has finished his prayer at
// the window (the faith thread: the design's 6.2). The greeting; four choices (the window; how he came to Rome; what he
// prays for; and, only after that one, the heart); the prayer side by side; the blessing, which goes three ways; the Son's
// line to us as he walks away. A second talk: one more line. The talk gives and needs nothing.
// ======================================================================================================
export const eleazarTree = (h = {}) => ({
  id: "eleazar",
  start: (g) => {
    if (is(g, "rome.blessed")) return "later";
    if (is(g, "rome.prayed")) return "blessing";                // (a talk cut short after the prayer goes on with the blessing)
    return is(g, "rome.metEleazar") ? "again" : "greet";
  },
  nodes: {
    // ---- "Peace to you, child." Four ways in, and every one comes to who the boy is.
    greet: {
      say: ["rome.eleazar.peace"],
      options: [
        { id: "peace", line: "rome.eleazar.opt.peace", set: "rome.metEleazar", then: "who" },
        { id: "waited", line: "rome.eleazar.opt.waited", say: ["rome.eleazar.waited"], set: "rome.metEleazar", then: "who" },
        { id: "church", line: "rome.eleazar.opt.church", say: ["rome.eleazar.church"], set: "rome.metEleazar", then: "who" },     // "A house of prayer." And that is all.
        { id: "yose", line: "rome.eleazar.opt.yose", when: (g) => is(g, "rome.metDateSeller"), say: ["rome.eleazar.yose.1", "rome.eleazar.yose.son", "rome.eleazar.yose.2"],
          set: "rome.metEleazar", then: "who" },
      ],
    },
    who: { say: ["rome.eleazar.who.1", "rome.eleazar.who.son.1", "rome.eleazar.who.son.2", "rome.eleazar.who.2"], then: "ask" },
    again: { say: ["rome.eleazar.again"], then: "ask" },
    ask: {
      options: [
        { id: "window", line: "rome.eleazar.opt.window", once: true, say: ["rome.eleazar.window.1", "rome.eleazar.window.son", "rome.eleazar.window.2"] },
        { id: "rome", line: "rome.eleazar.opt.rome", once: true, say: ["rome.eleazar.rome.1", "rome.eleazar.rome.2", "rome.eleazar.rome.3", "rome.eleazar.rome.son", "rome.eleazar.rome.4"] },
        { id: "prayFor", line: "rome.eleazar.opt.prayfor", once: true, say: ["rome.eleazar.prayfor.1", "rome.eleazar.prayfor.2", "rome.eleazar.prayfor.3", "rome.eleazar.prayfor.4"],
          then: async (g) => { await run(h.aside, g, true); return "simeon"; } },
        // the heart, only after "What do you pray for?"
        { id: "heart", line: "rome.eleazar.opt.heart", once: true, when: (g) => g.asked("eleazar/prayFor") > 0,
          say: ["rome.eleazar.heart.1", "rome.eleazar.heart.2", "rome.eleazar.heart.son.1", "rome.eleazar.heart.son.2", "rome.eleazar.heart.3"], then: "together" },
        { id: "tassels", line: "rome.eleazar.opt.tassels", once: true, say: ["rome.eleazar.tassels.1", "rome.eleazar.tassels.son", "rome.eleazar.tassels.2"] },
        // the boy went off before the prayer, and has come back to it
        { id: "waitAgain", line: "rome.eleazar.opt.waitagain", when: (g) => g.asked("eleazar/heart") > 0 && !is(g, "rome.prayed"), say: ["rome.eleazar.waitagain"], do: h.pray, then: "prayer" },
        { id: "bye", line: "rome.eleazar.opt.bye", say: { 1: ["rome.eleazar.bye.1"], more: ["rome.eleazar.bye.2"] }, then: "exit" },
      ],
    },
    // the Son, to us and not to him (Luke 2:25, Simeon, thought of and not named to the old man)
    simeon: { say: ["rome.eleazar.simeon"], then: async (g) => { await run(h.aside, g, false); return "back"; } },
    // "Shall we wait together a little?"
    together: {
      options: [
        { id: "together", line: "rome.eleazar.opt.together", do: h.pray, then: "prayer" },
        { id: "how", line: "rome.eleazar.opt.how", once: true, say: ["rome.eleazar.how"] },
        { id: "notNow", line: "rome.eleazar.opt.notnow", say: ["rome.eleazar.notnow"], then: "exit" },
      ],
    },
    // the prayer, side by side, facing toward Jerusalem (the boy's two lines are his own words)
    prayer: {
      say: ["rome.eleazar.prayer.son.1", "rome.eleazar.prayer.son.2", "rome.eleazar.amen"],
      then: async (g) => { await run(h.amen, g); g.flag("rome.prayed", true); return "prayed"; },
    },
    prayed: { say: ["rome.eleazar.prayed", "rome.eleazar.prayed.son"], then: "blessing" },
    // the blessing: his hand on the boy's head (Numbers 6:25), and the boy gives him the last part (Numbers 6:26)
    blessing: { say: ["rome.eleazar.bless.0"], then: async (g) => { await run(h.bless, g); return "verse"; } },
    verse: {
      say: ["rome.eleazar.bless.1"],
      then: async (g) => { await run(h.release, g); return heard(g, "rome.dateseller.bless.2") ? "pieces" : "named"; },
    },
    named: { say: ["rome.eleazar.bless.son"], then: "lastPart" },
    pieces: { say: ["rome.eleazar.bless.son", "rome.eleazar.pieces.son", "rome.eleazar.pieces"], then: "lastPart" },
    lastPart: {
      options: [
        { id: "last", line: "rome.eleazar.opt.last", say: ["rome.eleazar.last.son", "rome.eleazar.last"], set: "rome.blessed", then: "go" },
      ],
    },
    go: {
      say: ["rome.eleazar.go"],
      then: async (g) => { await run(h.rest, g); await run(h.away, g); return "walking"; },
    },
    walking: { say: ["rome.eleazar.walking"], then: "exit" },
    // ---- a second talk: he looks up from his scroll and nods; one line, and nothing more on later visits
    later: { say: ["rome.eleazar.later"] },
  },
});

// ======================================================================================================
// mariamTree: Mariam, his granddaughter, in the hen yard. Her hens (the chickens' thread: four lines, nobody explaining
// it); her grandfather; her father, who sells dates in the city; the words of the Law on the doorpost; a hen looked in the
// eye (hook crouch); and the Son's little sister.
// ======================================================================================================
export const mariamTree = (h = {}) => ({
  id: "mariam",
  start: (g) => (is(g, "rome.metMariam") ? "again" : "meet"),
  nodes: {
    meet: {
      options: [
        { id: "hens", line: "rome.mariam.opt.hens", say: ["rome.mariam.hens.1"], set: "rome.metMariam", then: "hens" },
        { id: "name", line: "rome.mariam.opt.name", say: ["rome.mariam.name"], set: "rome.metMariam", then: "ask" },
        { id: "window", line: "rome.mariam.opt.window", when: (g) => !is(g, "rome.eleazarDown"), say: ["rome.mariam.window"], set: "rome.metMariam", then: "ask" },
        { id: "bench", line: "rome.mariam.opt.bench", when: (g) => is(g, "rome.eleazarDown"), say: ["rome.mariam.bench"], set: "rome.metMariam", then: "ask" },
        { id: "boss", line: "rome.mariam.opt.boss", say: ["rome.mariam.boss.1", "rome.mariam.boss.son", "rome.mariam.boss.2"], set: "rome.metMariam", then: "ask" },
      ],
    },
    again: { say: ["rome.mariam.again"], then: "ask" },
    // the chickens' thread: they have stood in a row since first light; hens are sensible; Grandfather says they only look;
    // and the Son, to us, sees what they are looking at
    hens: {
      say: ["rome.mariam.hens.2", "rome.mariam.hens.3"],
      then: async (g) => { g.flag("rome.sawHens", true); await run(h.aside, g, true); return "door"; },
    },
    door: { say: ["rome.mariam.hens.son"], then: async (g) => { await run(h.aside, g, false); return "ask"; } },
    ask: {
      options: [
        { id: "hensAsk", line: "rome.mariam.opt.hens2", when: (g) => !is(g, "rome.sawHens"), say: ["rome.mariam.hens.1"], then: "hens" },
        { id: "crouch", clue: true, line: "rome.mariam.opt.crouch", say: { 1: ["rome.mariam.crouch.1"], more: ["rome.mariam.crouch.3"] }, do: h.crouch,
          then: (g) => (g.asked("mariam/crouch") === 1 ? "crouched" : null) },
        { id: "family", line: "rome.mariam.opt.family", say: ["rome.mariam.family.1", "rome.mariam.family.2"],
          then: (g) => (is(g, "rome.metDateSeller") && g.asked("mariam/family") === 1 ? "dates" : null) },
        { id: "doorpost", line: "rome.mariam.opt.doorpost", say: { 1: ["rome.mariam.doorpost.1", "rome.mariam.doorpost.son", "rome.mariam.doorpost.2", "rome.mariam.doorpost.son2"], more: ["rome.mariam.doorpost.3"] } },
        { id: "bossAsk", line: "rome.mariam.opt.boss", when: (g) => !g.asked("mariam/boss"), once: true, say: ["rome.mariam.boss.1", "rome.mariam.boss.son", "rome.mariam.boss.2"] },
        { id: "bye", line: "rome.mariam.opt.bye", say: { 1: ["rome.mariam.bye.1"], more: ["rome.mariam.bye.2"] }, then: "exit" },
      ],
    },
    crouched: { say: ["rome.mariam.crouch.2"], then: "back" },
    dates: { say: ["rome.mariam.dates.son", "rome.mariam.dates"], then: "back" },
  },
});

// ======================================================================================================
// felixTree: Felix, Phyllis's son, a boatman (NEW 4's middle). The barges between here and Ostia; Corinth (and the Son at
// "Corinth", to us, stopping himself); his mother; and, with the lamp, his mother's wish, string, and his word.
// ======================================================================================================
export const felixTree = (h = {}) => ({
  id: "felix",
  start: (g) => (is(g, "rome.felixWord") ? "after" : is(g, "rome.metFelix") ? "again" : "meet"),
  nodes: {
    meet: {
      options: [
        { id: "felix", line: "rome.felix.opt.felix", when: (g) => g.has("lamp"), say: ["rome.felix.felix"], set: "rome.metFelix", then: "ask" },     // sent by his mother
        { id: "carry", line: "rome.felix.opt.carry", say: ["rome.felix.carry"], set: "rome.metFelix", then: "ask" },
        { id: "table", line: "rome.felix.opt.table", say: ["rome.felix.table"], set: "rome.metFelix", then: "ask" },
        { id: "where", line: "rome.felix.opt.where", say: ["rome.felix.where"], set: "rome.metFelix", then: "ask" },
      ],
    },
    again: { say: ["rome.felix.again"], then: "ask" },
    ask: {
      options: [
        // the lever: the lamp, from his mother
        { id: "lamp", line: "rome.felix.opt.lamp", when: (g) => g.has("lamp"), do: h.setDown, then: "gift" },
        { id: "name", line: "rome.felix.opt.name", when: (g) => !g.asked("felix/felix") && !g.asked("felix/name"), say: ["rome.felix.name"] },
        { id: "ostia", line: "rome.felix.opt.ostia", say: { 1: ["rome.felix.ostia.1", "rome.felix.ostia.2"], more: ["rome.felix.ostia.3"] } },
        { id: "corinth", line: "rome.felix.opt.corinth", say: { 1: ["rome.felix.corinth.1", "rome.felix.corinth.2"], more: ["rome.felix.corinth.3"] },
          then: async (g) => { if (g.asked("felix/corinth") !== 1) return null; await run(h.aside, g, true); return "paul"; } },
        { id: "mother", line: "rome.felix.opt.mother", when: (g) => is(g, "rome.metPhyllis") && !g.has("lamp"), say: { 1: ["rome.felix.mother.1", "rome.felix.mother.2"], more: ["rome.felix.mother.3"] } },
        { id: "bye", line: "rome.felix.opt.bye", say: { 1: ["rome.felix.bye.1"], more: ["rome.felix.bye.2"] }, then: "exit" },
      ],
    },
    // "Corinth!": the Son, to us, and stopping himself. (Then straight back to the menu he came from: "back" from paul2
    // would be paul.)
    paul: { say: ["rome.felix.paul.son.1", "rome.felix.paul.son.2"], then: async (g) => { await run(h.aside, g, false); return "paul2"; } },
    paul2: { say: ["rome.felix.paul", "rome.felix.paul.son.3"], then: (g) => (is(g, "rome.felixWord") ? "afterAsk" : "ask") },
    // the lamp, and his mother's wish
    gift: {
      say: ["rome.felix.gift.1", "rome.felix.gift.son.1", "rome.felix.gift.2", "rome.felix.gift.3", "rome.felix.gift.son.2"],
      options: [
        { id: "come", line: "rome.felix.opt.come", do: h.lamp, then: "word" },
        { id: "string", line: "rome.felix.opt.string", once: true, say: ["rome.felix.string", "rome.felix.string.son"] },
      ],
    },
    word: { say: ["rome.felix.word.1", "rome.felix.word.2", "rome.felix.word.son"], then: "exit" },
    // ---- after his word
    after: { say: ["rome.felix.after"], then: "afterAsk" },
    afterAsk: {
      options: [
        { id: "corinthAfter", line: "rome.felix.opt.corinth", when: (g) => !g.asked("felix/corinth"), once: true, say: ["rome.felix.corinth.1", "rome.felix.corinth.2"],
          then: async (g) => { await run(h.aside, g, true); return "paul"; } },
        { id: "byeAfter", line: "rome.felix.opt.bye", say: ["rome.felix.bye.after"], then: "exit" },
      ],
    },
  },
});

/** Every tree, by name, for the tests. */
export const trees = { gaulTree, phyllisTree, titusTree, anserTree, eleazarTree, mariamTree, felixTree };

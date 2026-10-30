// The talks of Act Six's second and third legs (WRITE-20B: new in round twenty; briefs/WRITE-20.md, and the design,
// briefs/out/edo-design.md, puzzles #25 to #30). Plain data in the engine's format (docs/DESIGN.md, section 7, "Dialogue
// trees"), made as js/content/talk/nevada.js and talk/office.js make them: every word is a line id
// (js/content/lines/edo-b.en.js). An option's `line` is said by the one it belongs to (one of the three: a tree whose
// start branches by the lead offers each lead her own lines); its `say` is the reply (a list, or { 1, 2, more } by how many
// times it has been picked); `set` makes facts true; `do` is a script; `then` goes to a node, "back", "root" or "exit"
// (or is a function of the game giving one). WRITE-20A's trees (Yui's people) are in talk/edo-a.js; MERGE-20 joins the two
// into talk/edo.js.
//
// Each tree is a function of a `hooks` object, so that the scene hands in the scripts a branch needs:
//     import { roomTree } from "../talk/edo-b.js";
//     const ROOM = roomTree({ pray, openAltar, laugh, settle });
//     ...  use: (g) => g.talk(ROOM)
// A hook that is not handed in is passed over (the talk still says every line and sets every fact).
//
// THE HOOKS, and what each must do. None of them says a line the tree says.
//   roomTree (edo-chapel, #26: the three of them at the ladder's foot; Jinsuke with his arms out, Sei, O-Rin behind)
//     pray(g)       Little Sister folds her hands (actor.pray) before edo.chapel.pray.lilsis; the others still. Staging.
//     openAltar(g)  Grandmother Sei opens the closet altar: the cut-out's open state, the lamps' light on the Kannon.
//                   (The tree sets edo.altarOpen after it.)
//     laugh(g)      O-Rin laughs out loud once and covers her mouth (after edo.chapel.laugh.2). Staging.
//     settle(g)     the night: the lamps go down, the family on the mats (the tree has said edo.chapel.night.*; it sets
//                   edo.trusted before calling this). The scene's own morning follows.
//   seiTree, jinsukeTree, orinTree (edo-chapel, after edo.trusted: each of them, asked)
//     showLight(g)  orinTree: O-Rin presses the end of the pink flashlight: it comes on in her hands (edo.chapel.orin.light.3).
//                   Staging; the light is Little Sister's and stays hers (she leaves it on, on the mats: #27's pink floor).
//   isukeTree (edo-storehouse, #27: the constable at the door; Jinsuke and the two girls; Mom below, unasked)
//     letIn(g)      Jinsuke unbars the door and Isuke comes in to his mark `isuke`, dripping. Staging.
//     giveEgg(g)    Little Sister gives him the egg: g.take("egg") from her; he holds it in both hands. (The tree sets
//                   edo.eggGiven.) giveSushi(g) the same with "sushibox", if she has no egg (edo.sushiGiven).
//     goes(g)       he goes out and down the path in the rain, the egg in both hands. (The tree sets edo.constableGone.)
//     If Mom is the lead when the tree starts, it says edo.store.isuke.use.mom and ends: the scene keeps her below.
//   mirrorTree (edo-chapel, #27's end: no choices; the scene starts it when the family is down again, with the sun on the ladder)
//     sunOnMirror(g)  Sei takes the mirror off its stand and tilts it into the sun from the open trapdoor: the beam, the
//                   patch on the earth wall, the cross in it (ENGINE-20's mirror light). Before edo.chapel.show.3.
//     giveMirror(g) the mirror into Mom's hands: g.give("mirror", "mom") (the patch goes). After edo.chapel.give.4.
//     giveTrowel(g) Jinsuke's trowel: g.give("trowel", "mom"). After edo.chapel.trowel.2.
//     (The tree sets edo.mirror at its end, after "Then we go to Himeji.")
//   tomezoTree (edo-castle, #28: Tomezō up his ladder at `tomezo`, then down at `ladder`)
//     down(g)       he climbs down the ladder (after Little Sister's holler). (The tree sets edo.tomezoDown.)
//     trowel(g)     Mom holds out the trowel; he takes it: g.take("trowel"). (The tree sets edo.trowelBack.)
//     dress(g)      head-cloths and buckets: g.dress of the three to "edo-crew", a bucket each (no item: the outfit carries
//                   it, or the scene's cut-outs). (The tree sets edo.crew.)
//   guardTree (edo-castle, the gate; before edo.crew they ask, with it they count)
//     count(g)      the eight go up the ramp and through, counted (the scene walks them; the lines are the tree's).
//                   Must end with the family inside: the scene changes to edo-keep. (The tree sets edo.inside before it.)
//   shinnosukeTree (edo-keep, #29: the warden at the foot of the stairs)
//     show(g)       Little Sister switches the flashlight on in his face (after edo.keep.shin.opt.light). Staging.
//     lend(g)       the light into his hands: g.pass("lilflash", "shinnosuke") or the scene's equivalent; he holds it in
//                   both hands from here to the end of the act. (The tree sets edo.up after it: the stairs are open.)
//   topTree (edo-keeptop, #30: he kneels to a tall woman in a pale kimono with a mirror)
//     kneel(g)      he goes to his knees (before edo.top.truth.1); stand(g) he gets up (after the stand option, or the truth).
//     window(g)     he lifts the bar of the west shutters: the shutters' open state, the low sun across the floor to the
//                   east wall (ENGINE-20's beam). (The tree sets edo.window after it.)
//   doorTree (edo-keeptop, #30's end: no choices; the scene starts it when the mirror is used on the hum with edo.window)
//     patch(g)      the mirror's light on the hum: a hand-sized patch, the shimmer flaring into rings, the letterbox.
//     back(g)       Mom backs across the room to `farwest`, the patch growing with every step, to a doorway, the cross in it.
//     coin(g)       the coin into Mom's hand from whoever has it (g.take / g.give), after the giver's line.
//     giveMirror(g) the mirror into Shinnosuke's hands: g.take("mirror") from Mom. (The tree sets edo.door at its end.)
//
// THE FACTS. Set by the trees: edo.roomMet, edo.prayed, edo.altarOpen, edo.verse, edo.laughed, edo.trusted (#26);
// edo.eggGiven, edo.sushiGiven, edo.constableGone (#27); edo.mirror (#27's end); edo.tomezoDown, edo.trowelBack, edo.crew,
// edo.inside (#28); edo.lightShown, edo.up (#29); edo.truth, edo.window, edo.door (#30). Set by the scenes, and read here:
// edo.hidden (#25), edo.watch (O-Rin has warned: the constable is on the path), edo.ready (the mat and sacks are over the
// trapdoor, the pink light is off, and Mom is below: the scene's own test). And g.has("egg"), g.has("sushibox"),
// g.has("trowel"), g.has("lilflash"), g.has("coin"), g.has("mirror") (the one talking has it), g.asked("<tree>/<option>").
//
// Besides the trees: NOT_READY (what Jinsuke says if the constable is let in before the room is ready: a map by what is
// wrong), CLIMB (the stairs, floor by floor), the cards' and the step's line lists for SCENES-20, and `trees`, every tree by
// name, for the tests. S/work-20-writeB/ids.md says when each line is said.

const who = (g) => g.store.data.active;
const is = (g, fact) => !!g.flag(fact);
const run = async (g, hook) => { if (typeof hook === "function") await hook(g); };

// ======================================================================================================
// roomTree: #26, Our Father. Nobody can say the true thing first, because saying it could cost a life. Mom's openings are
// true and ask nothing; Big Sister notices the hinges; Little Sister notices O-Rin's hands. The way through is the
// family doing what it does at bedtime, out loud: each lead has a line that gets there, and it is always Little Sister who
// prays. Then the altar, what each thing is, the one line about Osaka, and the verse Mom gives the grandmother.
// ======================================================================================================
export const roomTree = (h = {}) => {
  const prayers = async (g) => { await run(g, h.pray); g.flag("edo.prayed", true); return "prayed"; };
  const opened = async (g) => { await run(g, h.openAltar); g.flag("edo.altarOpen", true); return "altar"; };
  return {
    id: "room",
    start: (g) => (is(g, "edo.trusted") ? "after" : is(g, "edo.altarOpen") ? "altar" : is(g, "edo.roomMet") ? "talk" : "meet"),
    nodes: {
      meet: { say: ["edo.chapel.meet.1", "edo.chapel.meet.2", "edo.chapel.meet.3", "edo.chapel.meet.4"],
        then: (g) => { g.flag("edo.roomMet", true); return "talk"; } },
      talk: {
        options: [
          // Mom: three true openings, and the wrong foot
          { id: "strangers", line: "edo.chapel.room.opt.strangers", when: (g) => who(g) === "mom", say: ["edo.chapel.room.strangers.1", "edo.chapel.room.strangers.2"] },
          { id: "sorry", line: "edo.chapel.room.opt.sorry", when: (g) => who(g) === "mom", say: ["edo.chapel.room.sorry.1", "edo.chapel.room.sorry.2"] },
          { id: "shelter", line: "edo.chapel.room.opt.shelter", when: (g) => who(g) === "mom", say: ["edo.chapel.room.shelter.1", "edo.chapel.room.shelter.2"] },
          { id: "what", line: "edo.chapel.room.opt.what", when: (g) => who(g) === "mom", say: ["edo.chapel.room.what.1", "edo.chapel.room.what.2", "edo.chapel.room.what.3"] },
          // Big Sister: the hinges (the clue that this is not a charcoal store), and her own wrong foot
          { id: "hinges", clue: true, line: "edo.chapel.room.opt.hinges", when: (g) => who(g) === "bigsis", say: ["edo.chapel.room.hinges.1", "edo.chapel.room.hinges.2", "edo.chapel.room.hinges.3"] },
          { id: "charcoal", line: "edo.chapel.room.opt.charcoal", when: (g) => who(g) === "bigsis", say: ["edo.chapel.room.charcoal.1", "edo.chapel.room.charcoal.2"] },
          // Little Sister: the hands (the clue), and a friend
          { id: "hands", clue: true, line: "edo.chapel.room.opt.hands", when: (g) => who(g) === "lilsis", say: ["edo.chapel.room.hands.1", "edo.chapel.room.hands.2", "edo.chapel.room.hands.3"] },
          { id: "friend", line: "edo.chapel.room.opt.friend", when: (g) => who(g) === "lilsis", say: ["edo.chapel.room.friend.1", "edo.chapel.room.friend.2"] },
          // the lever, one way for each lead: prayers, out loud, as at home
          { id: "prayersMom", line: "edo.chapel.room.opt.prayers.mom", when: (g) => who(g) === "mom", say: ["edo.chapel.room.prayers.mom.1", "edo.chapel.room.prayers.mom.2"], then: prayers },
          { id: "prayersBig", line: "edo.chapel.room.opt.prayers.bigsis", when: (g) => who(g) === "bigsis", say: ["edo.chapel.room.prayers.bigsis.1"], then: prayers },
          { id: "prayersLil", line: "edo.chapel.room.opt.prayers.lilsis", when: (g) => who(g) === "lilsis", say: ["edo.chapel.room.prayers.lilsis.1"], then: prayers },
        ],
      },
      // she says it in her clearest voice; a silence; the grandmother, very low, in the old words; the doors
      prayed: { say: ["edo.chapel.pray.lilsis", "edo.chapel.pray.sei", "edo.chapel.pray.bigsis", "edo.chapel.pray.mom", "edo.chapel.pray.open", "edo.chapel.pray.open.2", "edo.chapel.pray.open.3"], then: opened },
      altar: { say: ["edo.chapel.open.1", "edo.chapel.open.2", "edo.chapel.open.3"], then: "asked" },
      // the altar open: what each thing is, and the one line about Osaka; then the verse, which ends the evening
      asked: {
        options: [
          { id: "calendar", line: "edo.chapel.sei.opt.calendar", once: true, say: ["edo.chapel.sei.calendar.1", "edo.chapel.sei.calendar.2"] },
          { id: "water", line: "edo.chapel.sei.opt.water", once: true, say: ["edo.chapel.sei.water.1", "edo.chapel.sei.water.2", "edo.chapel.sei.water.3"] },
          { id: "priest", line: "edo.chapel.sei.opt.priest", once: true, say: ["edo.chapel.sei.priest.1", "edo.chapel.sei.priest.2", "edo.chapel.sei.priest.3", "edo.chapel.sei.priest.4"] },
          { id: "osaka", line: "edo.chapel.sei.opt.osaka", once: true, say: ["edo.chapel.sei.osaka.1", "edo.chapel.sei.osaka.2", "edo.chapel.sei.osaka.3"] },
          { id: "plan", line: "edo.chapel.sei.opt.plan", once: true, say: ["edo.chapel.sei.plan.1", "edo.chapel.sei.plan.2", "edo.chapel.sei.plan.3"] },
          { id: "orin", line: "edo.chapel.sei.opt.orin", once: true, say: ["edo.chapel.sei.orin.1", "edo.chapel.sei.orin.2", "edo.chapel.sei.orin.3"] },
          { id: "verse", line: "edo.chapel.sei.opt.verse", say: ["edo.chapel.verse.ask", "edo.chapel.verse.mom", "edo.chapel.verse.again", "edo.chapel.verse.mom", "edo.chapel.verse.sei", "edo.chapel.verse.after.1", "edo.chapel.verse.after.2"],
            set: "edo.verse", then: "laugh" },
        ],
      },
      // the first laugh in the room: O-Rin, out loud, once, and her hand over her mouth; then the night
      laugh: { say: ["edo.chapel.laugh.1", "edo.chapel.laugh.2"], then: async (g) => { await run(g, h.laugh); g.flag("edo.laughed", true); return "night"; } },
      night: { say: ["edo.chapel.laugh.3", "edo.chapel.night.1", "edo.chapel.night.2", "edo.chapel.night.3"],
        then: async (g) => { g.flag("edo.trusted", true); await run(g, h.settle); return "exit"; } },
      after: {},                                                   // (trusted: the people have their own trees now)
    },
  };
};

// ======================================================================================================
// seiTree: Grandmother Sei, after the family is trusted. The mirror (the plant for #27's end), her height, the calendar
// in her head, a thank-you for the Mary. Each lead has her own questions.
// ======================================================================================================
export const seiTree = (h = {}) => ({
  id: "sei",
  start: "talk",
  nodes: {
    talk: {
      options: [
        { id: "mirror", clue: true, line: "edo.chapel.sei.opt.mirror", when: (g) => who(g) === "mom" && !is(g, "edo.mirror"), say: ["edo.chapel.sei.mirror.1", "edo.chapel.sei.mirror.2"] },
        { id: "tall", line: "edo.chapel.sei.opt.tall", once: true, when: (g) => who(g) === "mom", say: ["edo.chapel.sei.tall.1", "edo.chapel.sei.tall.2", "edo.chapel.sei.tall.3"] },
        { id: "verse", line: "edo.chapel.sei.opt.verse", once: true, when: (g) => who(g) === "mom" && !is(g, "edo.verse"),
          say: ["edo.chapel.verse.ask", "edo.chapel.verse.mom", "edo.chapel.verse.again", "edo.chapel.verse.mom", "edo.chapel.verse.sei", "edo.chapel.verse.after.1", "edo.chapel.verse.after.2"], set: "edo.verse" },
        { id: "calendar", line: "edo.chapel.sei.opt.bigsis", once: true, when: (g) => who(g) === "bigsis", say: ["edo.chapel.sei.bigsis.1"] },
        { id: "priest", line: "edo.chapel.sei.opt.priest", once: true, when: (g) => who(g) === "bigsis" && g.asked("room/priest") === 0,
          say: ["edo.chapel.sei.priest.1", "edo.chapel.sei.priest.2", "edo.chapel.sei.priest.3", "edo.chapel.sei.priest.4"] },
        { id: "thanks", line: "edo.chapel.sei.opt.lilsis", once: true, when: (g) => who(g) === "lilsis", say: ["edo.chapel.sei.lilsis.1"] },
        { id: "orin", line: "edo.chapel.sei.opt.orin", once: true, when: (g) => who(g) === "lilsis" && g.asked("room/orin") === 0, say: ["edo.chapel.sei.orin.1", "edo.chapel.sei.orin.2", "edo.chapel.sei.orin.3"] },
        { id: "bye", line: "edo.chapel.sei.bye.mom", say: ["edo.chapel.sei.bye"], then: "exit" },
      ],
    },
  },
});

// ======================================================================================================
// jinsukeTree: Jinsuke, trusted. The water he keeps, O-Rin's watch, the cousin at Himeji (the trowel's plant), and why he
// does not lie either (the plan for the constable: truth, and not much of it).
// ======================================================================================================
export const jinsukeTree = (h = {}) => ({
  id: "jinsuke",
  start: "talk",
  nodes: {
    talk: {
      options: [
        { id: "water", line: "edo.chapel.jinsuke.opt.water", once: true, when: (g) => who(g) === "mom", say: ["edo.chapel.jinsuke.water.1"] },
        { id: "lie", clue: true, line: "edo.chapel.jinsuke.opt.lie", when: (g) => who(g) === "mom" && !is(g, "edo.constableGone"), say: ["edo.chapel.jinsuke.lie.1", "edo.chapel.jinsuke.lie.2", "edo.chapel.jinsuke.lie.3"] },
        { id: "osaka", line: "edo.chapel.sei.opt.osaka", once: true, when: (g) => who(g) === "mom" && g.asked("room/osaka") === 0, say: ["edo.chapel.sei.osaka.1", "edo.chapel.sei.osaka.2", "edo.chapel.sei.osaka.3"] },
        { id: "plan", line: "edo.chapel.sei.opt.plan", once: true, when: (g) => who(g) === "mom" && g.asked("room/plan") === 0, say: ["edo.chapel.sei.plan.1", "edo.chapel.sei.plan.2", "edo.chapel.sei.plan.3"] },
        { id: "watch", line: "edo.chapel.jinsuke.opt.watch", once: true, when: (g) => who(g) === "bigsis", say: ["edo.chapel.jinsuke.watch.1", "edo.chapel.jinsuke.watch.2"] },
        { id: "cousin", clue: true, line: "edo.chapel.jinsuke.opt.cousin", when: (g) => who(g) === "lilsis" && !is(g, "edo.mirror"), say: ["edo.chapel.jinsuke.cousin.1", "edo.chapel.jinsuke.cousin.2", "edo.chapel.jinsuke.cousin.3"] },
        { id: "bye", line: "edo.chapel.jinsuke.bye.mom", say: ["edo.chapel.jinsuke.bye"], then: "exit" },
      ],
    },
  },
});

// ======================================================================================================
// orinTree: O-Rin. With Little Sister, two girls whispering (the whisper, the chickens, the light with no fire, and her
// prayer, a little louder); with the others, briefly.
// ======================================================================================================
export const orinTree = (h = {}) => ({
  id: "orin",
  start: "talk",
  nodes: {
    talk: {
      options: [
        { id: "whisper", line: "edo.chapel.orin.opt.whisper", once: true, when: (g) => who(g) === "lilsis", say: ["edo.chapel.orin.whisper.1", "edo.chapel.orin.whisper.2"] },
        { id: "chickens", line: "edo.chapel.orin.opt.chickens", once: true, when: (g) => who(g) === "lilsis", say: ["edo.chapel.orin.chickens.1", "edo.chapel.orin.chickens.2"] },
        { id: "light", line: "edo.chapel.orin.opt.light", once: true, when: (g) => who(g) === "lilsis" && g.has("lilflash"),
          say: ["edo.chapel.orin.light.1", "edo.chapel.orin.light.2"], do: h.showLight, then: "lit" },
        { id: "pray", line: "edo.chapel.orin.opt.pray", once: true, when: (g) => who(g) === "lilsis" && is(g, "edo.trusted"), say: ["edo.chapel.orin.pray.1", "edo.chapel.orin.pray.2"] },
        { id: "mom", line: "edo.chapel.orin.opt.mom", once: true, when: (g) => who(g) === "mom", say: ["edo.chapel.orin.mom.1", "edo.chapel.orin.mom.2"] },
        { id: "bigsis", line: "edo.chapel.orin.opt.bigsis", once: true, when: (g) => who(g) === "bigsis", say: ["edo.chapel.orin.bigsis.1", "edo.chapel.orin.bigsis.2"] },
        { id: "bye", line: "edo.chapel.orin.bye.lilsis", say: ["edo.chapel.orin.bye"], then: "exit" },
      ],
    },
    lit: { say: ["edo.chapel.orin.light.3"], then: "talk" },
  },
});

/** What Jinsuke says if the constable is let in before the room is ready: by what is wrong (the scene's test). */
export const NOT_READY = { mat: "edo.store.notready.mat", pink: "edo.store.notready.pink", mom: "edo.store.notready.mom" };

// ======================================================================================================
// isukeTree: #27, Charcoal, And A Kind Child. The constable's man at the door: wet, hungry, sleepy, polite. Jinsuke lets
// him in; he asks; the two girls answer, every answer true (Big Sister's wrong foot is answering a question he has not
// asked). The lever is the egg, given freely. "Nothing here but charcoal and a kind child."
// ======================================================================================================
export const isukeTree = (h = {}) => {
  const given = (flag, hook) => async (g) => { await run(g, hook); g.flag(flag, true); return "goes"; };
  return {
    id: "isuke",
    start: (g) => (who(g) === "mom" ? "momNo" : "door"),
    nodes: {
      momNo: { say: ["edo.store.isuke.use.mom"] },
      door: { say: ["edo.store.isuke.in.1"], then: async (g) => { await run(g, h.letIn); return "in"; } },
      in: { say: ["edo.store.isuke.in.2", "edo.store.isuke.in.3", "edo.store.isuke.in.3b", "edo.store.isuke.in.4", "edo.store.isuke.in.5", "edo.store.isuke.in.6"], then: "asked" },
      asked: {
        options: [
          // Big Sister: the sea (the design's), the east, the wrong foot, the record
          { id: "sea", line: "edo.store.isuke.opt.sea", once: true, when: (g) => who(g) === "bigsis", say: ["edo.store.isuke.sea.1", "edo.store.isuke.sea.2", "edo.store.isuke.sea.3"] },
          { id: "east", line: "edo.store.isuke.opt.east", once: true, when: (g) => who(g) === "bigsis", say: ["edo.store.isuke.east.1", "edo.store.isuke.east.2"] },
          { id: "mom", line: "edo.store.isuke.opt.mom", once: true, when: (g) => who(g) === "bigsis", say: ["edo.store.isuke.mom.1", "edo.store.isuke.mom.2", "edo.store.isuke.mom.3", "edo.store.isuke.mom.4"] },
          { id: "tall", line: "edo.store.isuke.opt.tall", once: true, when: (g) => who(g) === "bigsis", say: ["edo.store.isuke.tall.1", "edo.store.isuke.tall.2"] },
          // Little Sister: hats, the church, the yawns, the boots; and the egg
          { id: "hat", line: "edo.store.isuke.opt.hat", once: true, when: (g) => who(g) === "lilsis", say: ["edo.store.isuke.hat.1"] },
          { id: "temple", line: "edo.store.isuke.opt.temple", once: true, when: (g) => who(g) === "lilsis", say: ["edo.store.isuke.temple.1", "edo.store.isuke.temple.2"] },
          { id: "sleepy", line: "edo.store.isuke.opt.sleepy", once: true, when: (g) => who(g) === "lilsis", say: ["edo.store.isuke.sleepy.1"] },
          { id: "boots", line: "edo.store.isuke.opt.boots", once: true, when: (g) => who(g) === "lilsis", say: ["edo.store.isuke.boots.1"] },
          { id: "egg", line: "edo.store.isuke.opt.egg", when: (g) => who(g) === "lilsis" && g.has("egg"),
            say: ["edo.store.isuke.egg.1", "edo.store.isuke.egg.2", "edo.store.isuke.egg.3"], then: given("edo.eggGiven", h.giveEgg) },
          { id: "sushi", line: "edo.store.isuke.opt.sushi", when: (g) => who(g) === "lilsis" && !g.has("egg") && g.has("sushibox"),
            say: ["edo.store.isuke.sushi.1", "edo.store.isuke.sushi.2"], then: given("edo.sushiGiven", h.giveSushi) },
        ],
      },
      goes: { say: ["edo.store.isuke.go.1", "edo.store.isuke.go.2", "edo.store.isuke.go.3", "edo.store.isuke.go.4", "edo.store.isuke.go.5"],
        then: async (g) => { g.flag("edo.constableGone", true); await run(g, h.goes); return "after"; } },
      after: { say: ["edo.store.after.1", "edo.store.after.2", "edo.store.after.3", "edo.store.after.4"], then: "exit" },
    },
  };
};

// ======================================================================================================
// mirrorTree: #27's end. Below, in the morning sun down the trapdoor: the grandmother's mirror, the cross in its light, Big
// Sister's physics (and the one thing she has no physics for), the gift; Jinsuke's trowel; the castle's two stories;
// "That's a door." "Then we go to Himeji." No choices.
// ======================================================================================================
export const mirrorTree = (h = {}) => ({
  id: "mirror",
  start: "show",
  nodes: {
    show: { say: ["edo.chapel.show.1", "edo.chapel.show.2"], then: async (g) => { await run(g, h.sunOnMirror); return "cross"; } },
    cross: { say: ["edo.chapel.show.3", "edo.chapel.show.4", "edo.chapel.show.5", "edo.chapel.show.6", "edo.chapel.show.7", "edo.chapel.show.8",
      "edo.chapel.give.1", "edo.chapel.give.2", "edo.chapel.give.3", "edo.chapel.give.4"], then: async (g) => { await run(g, h.giveMirror); return "trowel"; } },
    trowel: { say: ["edo.chapel.trowel.1", "edo.chapel.trowel.2"], then: async (g) => { await run(g, h.giveTrowel); return "stories"; } },
    stories: { say: ["edo.chapel.trowel.3", "edo.chapel.trowel.4", "edo.chapel.story.1", "edo.chapel.story.2", "edo.chapel.story.2b", "edo.chapel.story.3",
      "edo.chapel.story.4", "edo.chapel.story.5", "edo.chapel.story.6", "edo.chapel.story.7", "edo.chapel.story.8"],
      then: (g) => { g.flag("edo.mirror", true); return "exit"; } },
  },
});

// ======================================================================================================
// tomezoTree: #28, Eight At The Gate. Up the ladder he cannot hear anyone over himself: courtesy does not carry, waiting
// does not work, hollering does. Down, he wants a reason he can hold: the trowel is one. Then three hands, head-cloths,
// buckets, and how the gate counts.
// ======================================================================================================
export const tomezoTree = (h = {}) => ({
  id: "tomezo",
  start: (g) => (is(g, "edo.tomezoDown") ? (is(g, "edo.trowelBack") ? "crew" : "down") : "up"),
  nodes: {
    up: {
      say: ["edo.castle.tomezo.shout.1", "edo.castle.tomezo.shout.2"],
      options: [
        { id: "polite", line: "edo.castle.tomezo.opt.polite", when: (g) => who(g) === "mom", say: ["edo.castle.tomezo.polite.1", "edo.castle.tomezo.polite.2"] },
        { id: "wait", line: "edo.castle.tomezo.opt.wait", when: (g) => who(g) === "bigsis", say: ["edo.castle.tomezo.wait.1", "edo.castle.tomezo.wait.2"] },
        { id: "holler", clue: true, line: "edo.castle.tomezo.opt.holler", when: (g) => who(g) === "lilsis",
          say: ["edo.castle.tomezo.holler.1", "edo.castle.tomezo.holler.2", "edo.castle.tomezo.holler.3"],
          then: async (g) => { g.flag("edo.tomezoDown", true); await run(g, h.down); return "met"; } },
      ],
    },
    met: { say: ["edo.castle.tomezo.down.1"], then: "down" },
    down: {
      options: [
        { id: "trowel", line: "edo.castle.tomezo.opt.trowel", when: (g) => g.has("trowel"),
          say: ["edo.castle.tomezo.trowel.1", "edo.castle.tomezo.trowel.2", "edo.castle.tomezo.trowel.3", "edo.castle.tomezo.trowel.4", "edo.castle.tomezo.trowel.5", "edo.castle.tomezo.trowel.6"],
          then: async (g) => { await run(g, h.trowel); g.flag("edo.trowelBack", true); return "hands"; } },
        { id: "helpNo", clue: true, line: "edo.castle.tomezo.opt.help", when: (g) => who(g) === "mom" && !g.has("trowel"), say: ["edo.castle.tomezo.help.no.1", "edo.castle.tomezo.help.no.2"] },
        { id: "ghost", line: "edo.castle.tomezo.opt.ghost", once: true, when: (g) => who(g) === "lilsis", say: ["edo.castle.tomezo.ghost.1"] },
        { id: "ise", line: "edo.castle.tomezo.opt.ise", once: true, when: (g) => who(g) === "mom", say: ["edo.castle.tomezo.ise.1"] },
        { id: "lime", line: "edo.castle.tomezo.opt.lime", once: true, when: (g) => who(g) === "bigsis", say: ["edo.castle.tomezo.lime.1", "edo.castle.tomezo.lime.2"] },
        { id: "bye", line: "edo.castle.tomezo.bye.mom", say: ["edo.castle.tomezo.bye"], then: "exit" },
      ],
    },
    // three hands short, three hands here: head-cloths and buckets (the hook dresses them)
    hands: { say: ["edo.castle.tomezo.help.1", "edo.castle.tomezo.help.2", "edo.castle.tomezo.help.3", "edo.castle.tomezo.help.4"],
      then: async (g) => { await run(g, h.dress); g.flag("edo.crew", true); return "crew"; } },
    crew: {
      options: [
        { id: "gate", clue: true, line: "edo.castle.tomezo.opt.gate", when: (g) => !is(g, "edo.inside"), say: ["edo.castle.tomezo.gate.1", "edo.castle.tomezo.gate.2", "edo.castle.tomezo.gate.3"] },
        { id: "keep", line: "edo.castle.tomezo.opt.keep", once: true, when: (g) => who(g) === "mom", say: ["edo.castle.tomezo.keep.1", "edo.castle.tomezo.keep.2"] },
        { id: "ghost2", line: "edo.castle.tomezo.opt.ghost", once: true, when: (g) => who(g) === "lilsis" && g.asked("tomezo/ghost") === 0, say: ["edo.castle.tomezo.ghost.1"] },
        { id: "ise2", line: "edo.castle.tomezo.opt.ise", once: true, when: (g) => who(g) === "mom" && g.asked("tomezo/ise") === 0, say: ["edo.castle.tomezo.ise.1"] },
        { id: "lime2", line: "edo.castle.tomezo.opt.lime", once: true, when: (g) => who(g) === "bigsis" && g.asked("tomezo/lime") === 0, say: ["edo.castle.tomezo.lime.1", "edo.castle.tomezo.lime.2"] },
        { id: "thanks", line: "edo.castle.tomezo.bye.lilsis", when: (g) => who(g) === "lilsis", say: ["edo.castle.tomezo.bye.lilsis.2"], then: "exit" },
        { id: "bye2", line: "edo.castle.tomezo.bye.mom", when: (g) => who(g) !== "lilsis", say: ["edo.castle.tomezo.bye"], then: "exit" },
      ],
    },
  },
});

// ======================================================================================================
// guardTree: the gate. Before the crew: name, house, business; Mom will not lie and cannot answer, so they leave (the
// ramp is free). With the crew: eight went out, eight come in, and the count is right. Nobody lies.
// ======================================================================================================
export const guardTree = (h = {}) => ({
  id: "guards",
  start: (g) => (is(g, "edo.inside") ? "in" : is(g, "edo.crew") ? "count" : "ask"),
  nodes: {
    ask: {
      say: ["edo.castle.guard.ask.1", "edo.castle.guard.ask.2", "edo.castle.guard.ask.3"],
      options: [
        { id: "traveller", line: "edo.castle.guard.opt.traveller", when: (g) => who(g) === "mom", say: ["edo.castle.guard.traveller.1", "edo.castle.guard.traveller.2"] },
        { id: "look", line: "edo.castle.guard.opt.look", once: true, when: (g) => who(g) === "mom", say: ["edo.castle.guard.look.1", "edo.castle.guard.look.2"] },
        { id: "count", clue: true, line: "edo.castle.guard.opt.count", when: (g) => who(g) === "bigsis", say: ["edo.castle.guard.count.1", "edo.castle.guard.count.2", "edo.castle.guard.count.3", "edo.castle.guard.count.4"] },
        { id: "swords", line: "edo.castle.guard.opt.swords", once: true, when: (g) => who(g) === "lilsis", say: ["edo.castle.guard.swords.1", "edo.castle.guard.swords.2", "edo.castle.guard.swords.3"] },
        { id: "tile", line: "edo.castle.guard.opt.tile", once: true, when: (g) => who(g) === "lilsis", say: ["edo.castle.guard.tile.1", "edo.castle.guard.tile.2"] },
        { id: "leave", line: "edo.castle.guard.opt.leave", say: ["edo.castle.guard.leave.1"], then: "exit" },
      ],
    },
    // with the crew: the count (the hook walks the eight through, and the scene goes inside)
    count: { say: ["edo.castle.guard.crew.1", "edo.castle.guard.crew.2", "edo.castle.guard.crew.3", "edo.castle.guard.crew.4", "edo.castle.guard.crew.5",
      "edo.castle.guard.crew.6", "edo.castle.guard.crew.7", "edo.castle.guard.crew.8", "edo.castle.guard.crew.9"],
      then: async (g) => { g.flag("edo.inside", true); await run(g, h.count); return "exit"; } },
    in: {},
  },
});

// ======================================================================================================
// shinnosukeTree: #29, A Light That Needs No Fire. The warden at the foot of the stairs: three poems (and a fourth for
// the asking), the lady, the dare, no fire in the keep; Little Sister's flashlight, and the lending of it; the rule he
// finds in four seconds. Big Sister cannot stop counting syllables.
// ======================================================================================================
export const shinnosukeTree = (h = {}) => ({
  id: "shinnosuke",
  start: (g) => (is(g, "edo.up") ? "ready" : is(g, "edo.shinMet") ? "talk" : "meet"),
  nodes: {
    meet: { say: ["edo.keep.shin.meet.1", "edo.keep.shin.meet.1b", "edo.keep.shin.meet.2", "edo.keep.shin.meet.3"], then: (g) => { g.flag("edo.shinMet", true); return "talk"; } },
    talk: {
      options: [
        { id: "poem", clue: true, line: "edo.keep.shin.opt.poem",
          say: { 1: ["edo.keep.shin.poem.1a", "edo.keep.shin.poem.1b", "edo.keep.shin.poem.1c", "edo.keep.shin.poem.1d"],
                 2: ["edo.keep.shin.poem.2a", "edo.keep.shin.poem.2b", "edo.keep.shin.poem.2c", "edo.keep.shin.poem.2d"],
                 3: ["edo.keep.shin.poem.3a", "edo.keep.shin.poem.3b", "edo.keep.shin.poem.3c", "edo.keep.shin.poem.3d"],
                 more: ["edo.keep.shin.poem.4a", "edo.keep.shin.poem.4b", "edo.keep.shin.poem.4c", "edo.keep.shin.poem.4d"] } },
        { id: "lady", clue: true, line: "edo.keep.shin.opt.lady", when: (g) => who(g) === "mom", say: ["edo.keep.shin.lady.1", "edo.keep.shin.lady.1b", "edo.keep.shin.lady.2", "edo.keep.shin.lady.3"] },
        { id: "dare", line: "edo.keep.shin.opt.dare", once: true, when: (g) => who(g) === "bigsis", say: ["edo.keep.shin.dare.1", "edo.keep.shin.dare.1b", "edo.keep.shin.dare.2"] },
        { id: "fire", clue: true, line: "edo.keep.shin.opt.fire", when: (g) => who(g) === "bigsis", say: ["edo.keep.shin.fire.1", "edo.keep.shin.fire.1b", "edo.keep.shin.fire.2", "edo.keep.shin.fire.3"] },
        { id: "up", line: "edo.keep.shin.opt.up", once: true, when: (g) => who(g) === "lilsis", say: ["edo.keep.shin.up.no.1", "edo.keep.shin.up.no.2"] },
        { id: "carry", line: "edo.keep.shin.opt.carry", once: true, when: (g) => who(g) === "mom" && !is(g, "edo.lightShown"), say: ["edo.keep.shin.carry.no.1", "edo.keep.shin.carry.no.2"] },
        // the light with no fire: shown, then lent
        { id: "light", clue: true, line: "edo.keep.shin.opt.light", when: (g) => who(g) === "lilsis" && g.has("lilflash") && !is(g, "edo.lightShown"),
          do: h.show, say: ["edo.keep.shin.light.1", "edo.keep.shin.light.2", "edo.keep.shin.light.3", "edo.keep.shin.light.4"], set: "edo.lightShown" },
        { id: "lend", line: "edo.keep.shin.opt.lend", when: (g) => who(g) === "lilsis" && g.has("lilflash") && is(g, "edo.lightShown"),
          say: ["edo.keep.shin.lend.1", "edo.keep.shin.lend.2", "edo.keep.shin.lend.3", "edo.keep.shin.lend.4", "edo.keep.shin.lend.5"],
          then: async (g) => { await run(g, h.lend); g.flag("edo.up", true); return "ready"; } },
        // the wrong foot and the laugh: the girls' own poems
        { id: "mine", line: "edo.keep.shin.opt.mine", once: true, when: (g) => who(g) === "bigsis" && g.asked("shinnosuke/poem") > 0, say: ["edo.keep.shin.mine.1", "edo.keep.shin.mine.2", "edo.keep.shin.mine.3"] },
        { id: "chicken", line: "edo.keep.shin.opt.chicken", once: true, when: (g) => who(g) === "lilsis" && g.asked("shinnosuke/poem") > 0, say: ["edo.keep.shin.chicken.0", "edo.keep.shin.chicken.1", "edo.keep.shin.chicken.2"] },
        { id: "thanks", line: "edo.keep.shin.bye.lilsis", when: (g) => who(g) === "lilsis", say: ["edo.keep.shin.bye.lilsis.2"], then: "exit" },
        { id: "bye", line: "edo.keep.shin.bye.mom", when: (g) => who(g) !== "lilsis", say: ["edo.keep.shin.bye"], then: "exit" },
      ],
    },
    ready: { say: ["edo.keep.stairs.up.mom"], then: "exit" },      // the stairs are open: the scene's climb (CLIMB) takes it from here
  },
});

/** The climb, floor by floor: the scene's short walk-through after edo.up (one line a floor; six is the top). */
export const CLIMB = ["edo.keep.climb.1", "edo.keep.climb.2", "edo.keep.climb.3", "edo.keep.climb.4", "edo.keep.climb.5"];

// ======================================================================================================
// topTree: #30, The Lady Of The Keep: the truth. He kneels to a tall woman in a pale kimono with a mirror, and tells her the
// truth first, as the story says. Mom's answers are all true; the lever is the whole truth, offered unasked. Then the
// window: the bar is his to lift, and he lifts it.
// ======================================================================================================
export const topTree = (h = {}) => ({
  id: "top",
  start: (g) => (is(g, "edo.truth") ? "told" : is(g, "edo.knelt") ? "kneeling" : "kneel"),
  nodes: {
    kneel: { then: async (g) => { await run(g, h.kneel); g.flag("edo.knelt", true); return "ask"; } },
    ask: { say: ["edo.top.truth.1", "edo.top.truth.2", "edo.top.truth.2b", "edo.top.truth.3"], then: "kneeling" },
    kneeling: {
      options: [
        { id: "lady", line: "edo.top.truth.opt.lady", when: (g) => who(g) === "mom",
          say: ["edo.top.truth.lady.1", "edo.top.truth.lady.2", "edo.top.truth.lady.3", "edo.top.truth.lady.4"],
          then: async (g) => { g.flag("edo.truth", true); await run(g, h.stand); return "told"; } },
        { id: "look", line: "edo.top.truth.opt.look", once: true, when: (g) => who(g) === "mom", say: ["edo.top.truth.look.1", "edo.top.truth.look.2"] },
        { id: "stand", line: "edo.top.truth.opt.stand", once: true, when: (g) => who(g) === "mom", say: ["edo.top.truth.stand.1"], do: h.stand },
        { id: "dare", line: "edo.top.truth.opt.dare", once: true, when: (g) => who(g) === "mom", say: ["edo.top.truth.dare.1", "edo.top.truth.dare.2"] },
        { id: "bigsis", clue: true, line: "edo.top.truth.opt.bigsis", when: (g) => who(g) === "bigsis", say: ["edo.top.truth.bigsis.1", "edo.top.truth.bigsis.2"], then: "exit" },      // (MERGE-20: a way out: the girls' only button here)
        { id: "lilsis", clue: true, line: "edo.top.truth.opt.lilsis", when: (g) => who(g) === "lilsis", say: ["edo.top.truth.lilsis.1", "edo.top.truth.lilsis.2"], then: "exit" },
      ],
    },
    told: {
      options: [
        { id: "window", clue: true, line: "edo.top.truth.opt.window", when: (g) => who(g) === "mom" && !is(g, "edo.window"),
          say: ["edo.top.window.1", "edo.top.window.2"], then: async (g) => { await run(g, h.window); g.flag("edo.window", true); return "sun"; } },
        { id: "light", line: "edo.top.truth.opt.light", once: true, when: (g) => who(g) === "lilsis", say: ["edo.top.truth.light.1"] },
        { id: "bigsis2", line: "edo.top.truth.opt.bigsis", once: true, when: (g) => who(g) === "bigsis" && g.asked("top/bigsis") === 0, say: ["edo.top.truth.bigsis.1", "edo.top.truth.bigsis.2"] },
        { id: "bye", line: "edo.top.truth.bye.mom", say: ["edo.top.truth.bye"], then: "exit" },
      ],
    },
    sun: { say: ["edo.top.window.3", "edo.top.window.4"], then: "told" },
  },
});

// ======================================================================================================
// doorTree: #30's end, the mirror in the sunbeam. A hand-sized patch, a letterbox; Big Sister's convex fact; Mom backs
// into the west window and the door grows to a doorway with the cross in it; the coin into her hand; the mirror to the
// warden, for Tomezō. No choices. The scene starts it when the mirror is used on the hum with the west shutters open.
// ======================================================================================================
export const doorTree = (h = {}) => ({
  id: "door",
  start: "patch",
  nodes: {
    patch: { say: ["edo.top.mirror.1"], then: async (g) => { await run(g, h.patch); return "small"; } },
    small: { say: ["edo.top.mirror.2", "edo.top.mirror.3", "edo.top.mirror.4", "edo.top.mirror.5", "edo.top.mirror.6", "edo.top.mirror.6b"],
      then: async (g) => { await run(g, h.back); return "grown"; } },
    grown: { say: ["edo.top.mirror.7", "edo.top.mirror.8", "edo.top.mirror.9", "edo.top.mirror.10", "edo.top.mirror.11", "edo.top.mirror.11b", "edo.top.mirror.12"],
      then: (g) => (g.has("coin") && who(g) === "mom" ? "coinMom" : "coin") },
    // whoever holds the coin gives it to Mom (the lines by the holder; the scene's hook moves it)
    coin: { then: (g) => { const holder = coinHolder(g); return holder === "lilsis" ? "coinLil" : "coinBig"; } },
    coinBig: { say: ["edo.top.coin.bigsis"], then: async (g) => { await run(g, h.coin); return "coinMom"; } },
    coinLil: { say: ["edo.top.coin.lilsis"], then: async (g) => { await run(g, h.coin); return "coinMom"; } },
    coinMom: { say: ["edo.top.coin.mom", "edo.top.give.1", "edo.top.give.2", "edo.top.give.3", "edo.top.give.4"],
      then: async (g) => { await run(g, h.giveMirror); g.flag("edo.door", true); return "exit"; } },
  },
});
/** Who has the coin, if the engine can say (ENGINE-12's pockets by lead); Big Sister by default (she traded for it). */
function coinHolder(g) {
  try {
    for (const lead of ["lilsis", "bigsis", "mom"]) {
      const bag = g.store && g.store.data && g.store.data.inventory && g.store.data.inventory[lead];      // (MERGE-20: the pockets are `inventory`)
      if (Array.isArray(bag) && bag.includes("coin")) return lead;
    }
  } catch (e) { /* the default */ }
  return "bigsis";
}

/** The cut-scenes' line lists, for SCENES-20 (the cards and the step are the scripts'; the lines are here in order). */
export const WALK = { card: ["edo.walk.card", "edo.walk.card.2"], under: ["edo.walk.lilsis"] };
export const STEP = {
  title: "edo.step.title",
  places: ["edo.step.1", "edo.step.2", "edo.step.3"],
  prayer: ["edo.step.pray.1", "edo.step.pray.2", "edo.step.pray.3"],
  goodbyes: ["edo.step.4", "edo.step.5", "edo.step.6", "edo.step.7"],
  poem: ["edo.step.poem.1", "edo.step.poem.2", "edo.step.poem.3", "edo.step.poem.4"],
  card: "edo.step.card",
};

/** The hints by puzzle, staged: the scene's hint function picks the stage by the facts (ids.md has the rule for each). */
export const HINTS = {
  hidden: { stages: ["", ".2", ".3"], rule: "pipe not listened at (edo.pipeHeard): 1; door still barred (edo.unbarred): 2; else 3" },
  trusted: { stages: [""], rule: "one stage" },
  mirror: { stages: ["", ".2", ".3", ".4"], rule: "mat and sacks not over the trapdoor: 1; the pink light on below: 2; Mom not below: 3; the constable at the door: 4" },
  inside: { stages: ["", ".2", ".3", ".4"], rule: "Tomezō up the ladder: 1; trowel still carried: 2; not yet crew: 3; crew, at the gate: 4" },
  up: { stages: ["", ".2", ".3"], rule: "not met (edo.shinMet): 1; light not shown (edo.lightShown): 2; else 3" },
  door: { stages: ["", ".2", ".3", ".4", ".5"], rule: "truth not told: 1; window shut: 2; mirror not yet in the beam: 3; letterbox open, Mom not at farwest: 4; doorway open, coin not in Mom's hand: 5" },
};

/** Every tree, by name, for the tests. */
export const trees = { roomTree, seiTree, jinsukeTree, orinTree, isukeTree, mirrorTree, tomezoTree, guardTree, shinnosukeTree, topTree, doorTree };

// The talks of the Office's stage one, "Processing" (WRITE-17: new in round seventeen; briefs/WRITE-17.md, and the design,
// briefs/out/office-hq-design.md, section 4). Plain data in the engine's format (docs/DESIGN.md, section 7, "Dialogue
// trees"), made as js/content/talk/nevada.js makes them: every word is a line id (js/content/lines/office.en.js). An
// option's `line` is said by the one it belongs to (Grandpa Joe, in every tree here); its `say` is the reply (a list, or
// { 1, 2, more } by how many times it has been picked); `set` makes facts true; `do` is a script; `then` goes to a node,
// "back", "root" or "exit" (or is a function of the game giving one).
//
// Each tree is a function of a `hooks` object, so that the scene hands in the scripts a branch needs:
//     import { interviewTree } from "../talk/office.js";
//     const INTERVIEW = interviewTree({ suspend, mop });
//     ...  use: (g) => g.talk(INTERVIEW)
// A hook that is not handed in is passed over (the talk still says every line and sets every fact).
//
// THE HOOKS, and what each must do. None of them says a line the tree says; a hook that says lines says only those named here.
//   interviewTree (Interview Room C: Dale and Merle across the table, Grandpa Joe in his chair; #17)
//     mop(g)        Merle mops his forehead with his handkerchief (and Dale may loosen his tie a finger's width and put it
//                   back). Staging only: called by the answers given while the room is warming.
//     suspend(g)    #17's end, after SUSPEND has been said: they gather the questionnaire, get up, go out, and lock the door
//                   (the thermostat's script calls it too, after saying SUSPEND itself). Grandpa Joe alone; the scene then
//                   says office.room.alone.1 to .3 and he looks up at the vent. (The tree sets office.alone.)
//   ventTree (Grandpa Joe standing on the spare chair under the vent; Ranger at the grille over the room, `over-room`; #18, #19)
//     receiptUp(g)  he reaches up and pushes the receipt through the slats: g.pass("receipt", "ranger"). (The tree sets
//                   office.receiptUp after it.)
//   opalTree (Opal's visit: the key in the door, and Opal at her mark `opal` with the banjo in her arms; #18's end)
//     sign(g)       he signs her slip; she brings the stamp down (THUNK).
//     banjo(g)      she puts the banjo in his hands: g.give("banjo-broken"). (The tree sets office.banjoBack after it.)
//     leave(g)      she walks to the door.
//     gone(g)       she goes out, and locks it behind her (gently).
//   intercomTree (Grandpa Joe at the intercom by the door, alone; #19)
//     press(g)      he presses the button: the buzz, the button lit. Staging.
//     release(g)    he lets it go. Staging.
//     burger(g)     on every speaker in the building, await g.pa("office.pa.burger"); in the break room, Jed is up so fast
//                   the ice pack is still in the air, and he is gone (office.jed.go.1 to .3 where they can be heard: the
//                   hook says them if Ranger is looking down into the break room, and not otherwise). (The tree sets
//                   office.jedGone after it.)
//   ragTree (the door open, Dale and Merle in it and Wendell behind them; Grandpa Joe playing the pie-tin banjo; #20)
//     louder(g)     he plays louder. Staging and music.
//     stop(g)       he stops playing; they say their last line, lock the door again and go. Staging.
//     down(g)       the cut-scene "Going Down": g.cutscene("office-down"). (The tree sets office.down before it.)
//
// THE FACTS. Set by the trees: office.ivBegun and office.iv (a number: the questionnaire's place, an index into Q below),
// office.lamplighter (he has heard the word), office.alone (#17), office.metAtVent, office.planned (he has said what the
// banjo is for), office.jedTold (Ranger has told him Jed is watching the pie), office.receiptUp, office.banjoBack (#18),
// office.jedGone, office.down (#20). Set by the scenes, and read here: office.heat (a number: 72 until #16, then up to
// 81), office.acOff (#16), office.sawProperty and office.sawBreak (Ranger has looked down through that grille),
// office.pieEaten, office.tinClean, office.schedule (#19); and, for nowAndThen and paNowAndThen below, office.trash (the
// raccoon noted, #16) and office.peanuts (Ranger has his packet). And g.has(...) (the one talking has it),
// g.asked("<tree>/<option>"). One option id may stand in several nodes of a tree (the interview's "hot", "warm",
// "greenpage", "leave" and "pause" are in every question): the engine keeps one memory for it, which is what is wanted.
//
// Besides the trees: SUSPEND (#17's end, a list of lines), ventTalk (the two of them, in the engine's `talk` form),
// nowAndThen (what each place says by itself, by scene id) and paNowAndThen (Houston, now and then). S/work-17-write/ids.md
// says when each line is said.

const is = (g, fact) => !!g.flag(fact);
const heat = (g) => Number(g.flag("office.heat")) || 72;
const cool = (g) => heat(g) < 77;
const warm = (g) => heat(g) >= 77 && heat(g) < 81;
const hot = (g) => heat(g) >= 81;
/** Where Ranger is, if the engine can say (ENGINE-17's g.where): true when he is at the grille over the room. */
const rangerOver = (g) => { try { return typeof g.where === "function" && (g.where("ranger") || {}).mark === "over-room"; } catch (e) { return false; } };

/** #17's end, said by the tree (and by the thermostat's script, with the suits there, at 81): Regulation 9. */
export const SUSPEND = ["office.suspend.1", "office.suspend.2", "office.suspend.3", "office.suspend.4", "office.suspend.5"];

// ======================================================================================================
// interviewTree: #17, The Comfortable Room. Dale reads the questions off a questionnaire forty-seven pages long, Merle
// writes the answers down and apologizes for every question before Dale asks it, and Grandpa Joe answers how he likes:
// every answer true, one a funny wrong foot, one that gives him something, one just him. The clues: yesterday at 1747,
// the green page (Lamplighter), Opal, the receipt. It is never finished: the only way out is the heat (#16), and
// Regulation 9, asked about at 81, or his honest "One" when asked how comfortable he is.
// ======================================================================================================
const Q = ["q1", "q2", "q3", "q4", "q5", "q6", "m1", "m2", "m3", "m4", "m5"];
const at = (g) => Math.min(Q.length - 1, Math.max(0, Number(g.flag("office.iv")) || 0));
/** On to question n (and remember it, so that a talk begun again starts there). */
const to = (n) => (g) => { g.flag("office.iv", n); return Q[n]; };
const GREEN = ["office.iv.q5.strike", "office.iv.q5.green.1", "office.iv.q5.green.2", "office.iv.q5.green.3"];
const RECEIPT = ["office.iv.q6.receipt.1", "office.iv.q6.receipt.2", "office.iv.q6.receipt.3"];
const ROUND = ["office.iv.m5.a", "office.iv.m5.next.1", "office.iv.m5.next.2"];

export const interviewTree = (h = {}) => {
  // what he can say at any question: the lever (hot), its warning (warm), the green page, going home, and a minute's rest
  const common = [
    { id: "hot", line: "office.iv.opt.hot", when: hot, say: SUSPEND, set: "office.alone", do: h.suspend, then: "exit" },
    { id: "warm", line: "office.iv.opt.warm", when: warm, do: h.mop,
      say: { 1: ["office.room.thermostat.77.suits.1", "office.room.thermostat.77.suits.2", "office.room.thermostat.77.suits.3"], more: ["office.iv.warm.again"] } },
    { id: "greenpage", line: "office.iv.opt.greenpage", once: true, when: (g) => is(g, "office.lamplighter"), say: ["office.iv.green.1", "office.iv.green.2"] },
    { id: "leave", line: "office.iv.opt.leave", say: { 1: ["office.iv.leave.1", "office.iv.leave.2", "office.iv.leave.3"], more: ["office.iv.leave.again.1", "office.iv.leave.again.2"] } },
    { id: "pause", line: "office.iv.opt.pause", say: ["office.iv.pause"], then: "exit" },
  ];
  const ask = (say, options) => ({ say, options: [...options, ...common] });
  return {
    id: "interview",
    start: (g) => (is(g, "office.alone") ? "gone" : is(g, "office.ivBegun") ? "again" : "open"),
    nodes: {
      open: { say: ["office.iv.open.1", "office.iv.open.2", "office.iv.open.3", "office.iv.open.4", "office.iv.open.5"],
        then: (g) => { g.flag("office.ivBegun", true); return "q1"; } },
      again: { say: ["office.iv.again.1", "office.iv.again.2"], then: (g) => Q[at(g)] },
      gone: {},                                                     // (the suits have gone: nothing to say)

      // page one, question one: the name. He never says his last name is Grandpa; they write it down anyway.
      q1: ask(["office.iv.q1"], [
        { id: "joe", line: "office.iv.opt.joe", say: ["office.iv.q1.last"], then: "q1b" },
        { id: "drove", line: "office.iv.opt.drove", once: true, say: ["office.iv.q1.drove.1", "office.iv.q1.drove.2"] },
      ]),
      q1b: { options: [
        { id: "folks", line: "office.iv.opt.folks", say: ["office.iv.q1.folks"], then: "named" },
        { id: "sign", line: "office.iv.opt.sign", say: ["office.iv.q1.sign.1", "office.iv.q1.sign.2"], then: "named" },
        { id: "sooner", line: "office.iv.opt.sooner", say: ["office.iv.q1.sooner.1", "office.iv.q1.sooner.2"], then: "named" },
        ...common,
      ] },
      named: { say: ["office.iv.q1.record", "office.iv.q1.jolene"], then: to(1) },

      q2: ask(["office.iv.sorry", "office.iv.q2"], [
        { id: "lemonade", line: "office.iv.opt.lemonade", say: ["office.iv.q2.lemonade.1", "office.iv.q2.lemonade.2", "office.iv.q2.lemonade.3"], then: to(2) },
        { id: "rocks", line: "office.iv.opt.rocks", say: ["office.iv.q2.rocks.1", "office.iv.q2.rocks.2"], then: to(2) },
        { id: "road", line: "office.iv.opt.road", say: ["office.iv.q2.road"], then: to(2) },
      ]),

      // yesterday at 1747 (the clue: somebody wrote down the very minute); and Opal, who files his statements of nothing
      q3: ask(["office.iv.q3.sorry", "office.iv.q3"], [
        { id: "wagon", line: "office.iv.opt.wagon", say: ["office.iv.q3.wagon.1", "office.iv.q3.wagon.2", "office.iv.q3.wagon.3", "office.iv.q3.wagon.4"], then: to(3) },
        { id: "sector", line: "office.iv.opt.sector", say: ["office.iv.q3.sector.1", "office.iv.q3.sector.2", "office.iv.q3.sector.3", "office.iv.q3.sector.4"], then: to(3) },
        { id: "opal", line: "office.iv.opt.opal", say: ["office.iv.q3.opal.1", "office.iv.q3.opal.2", "office.iv.q3.opal.3"], then: to(3) },
        { id: "minute", line: "office.iv.opt.minute", once: true, say: ["office.iv.q3.minute.1", "office.iv.q3.minute.2", "office.iv.q3.minute.3"] },
      ]),

      // page two: the raccoon, who is not on the form, except on this one
      q4: ask(["office.iv.q4.page", "office.iv.sorry", "office.iv.q4"], [
        { id: "what", line: "office.iv.opt.what", say: { 1: ["office.iv.q4.what.1", "office.iv.q4.what.2", "office.iv.q4.what.3"], more: ["office.iv.q4.what.3"] } },
        { id: "handsome", line: "office.iv.opt.handsome", say: ["office.iv.q4.handsome.1", "office.iv.q4.handsome.2", "office.iv.q4.handsome.3"], then: to(4) },
        { id: "likeme", line: "office.iv.opt.likeme", say: ["office.iv.q4.likeme"], then: to(4) },
      ]),

      // the green page: Lamplighter (the clue: there is such a thing, and they do not know what it is either)
      q5: ask(["office.iv.q5.turn", "office.iv.sorry", "office.iv.q5"], [
        { id: "withwhat", line: "office.iv.opt.withwhat", say: GREEN, set: "office.lamplighter", then: to(5) },
        { id: "pleasure", line: "office.iv.opt.pleasure", say: GREEN, set: "office.lamplighter", then: to(5) },
        { id: "lamp", line: "office.iv.opt.lamp", say: ["office.iv.q5.lamp", ...GREEN.slice(1)], set: "office.lamplighter", then: to(5) },
      ]),

      // the banjo (he struck an officer with it once, and says so), and the receipt for it
      q6: ask(["office.iv.sorry", "office.iv.q6"], [
        { id: "once", line: "office.iv.opt.once", say: ["office.iv.q6.once.1", "office.iv.q6.once.2", ...RECEIPT], then: to(6) },
        { id: "sorry", line: "office.iv.opt.sorry", say: ["office.iv.q6.sorry.1", "office.iv.q6.sorry.2", ...RECEIPT], then: to(6) },
        { id: "going", line: "office.iv.opt.going", say: ["office.iv.q6.going", ...RECEIPT], then: to(6) },
      ]),

      // and on, and on: five more, round and round, never finished
      m1: ask(["office.iv.sorry", "office.iv.m1"], [
        { id: "m1a", line: "office.iv.opt.m1.a", say: ["office.iv.m1.a"], then: to(7) },
        { id: "m1b", line: "office.iv.opt.m1.b", say: ["office.iv.m1.b.1", "office.iv.m1.b.2"], then: to(7) },
      ]),
      m2: ask(["office.iv.sorry.2", "office.iv.m2"], [
        { id: "m2a", line: "office.iv.opt.m2.a", say: ["office.iv.m2.a"], then: to(8) },
        { id: "m2b", line: "office.iv.opt.m2.b", say: ["office.iv.m2.b"], then: to(8) },
      ]),
      m3: ask(["office.iv.sorry.3", "office.iv.m3"], [
        { id: "m3a", line: "office.iv.opt.m3.a", say: ["office.iv.m3.a"], then: to(9) },
        { id: "m3b", line: "office.iv.opt.m3.b", say: ["office.iv.m3.b"], then: to(9) },
      ]),
      m4: ask(["office.iv.sorry", "office.iv.m4"], [
        { id: "m4a", line: "office.iv.opt.m4.a", say: ["office.iv.m4.a"], then: to(10) },
        { id: "m4b", line: "office.iv.opt.m4.b", say: ["office.iv.m4.b"], then: to(10) },
      ]),
      // how comfortable, from one to five: at 81 his honest answer is the second way to Regulation 9
      m5: ask(["office.iv.sorry.4", "office.iv.m5"], [
        { id: "m5cool", line: "office.iv.opt.m5.cool", when: cool, say: ROUND, then: to(6) },
        { id: "m5warm", line: "office.iv.opt.m5.warm", when: warm, say: ROUND, do: h.mop, then: to(6) },
        { id: "m5hot", line: "office.iv.opt.m5.hot", when: hot, say: ["office.iv.m5.hot.1", "office.iv.m5.hot.2", ...SUSPEND], set: "office.alone", do: h.suspend, then: "exit" },
      ]),
    },
  };
};

// ======================================================================================================
// ventTree: Grandpa Joe on the spare chair, his face at the vent; Ranger at the grille over him. What they say to each
// other (Ranger thinks, and Joe says what he means), and the plan: the banjo, which will not come through the slats; the
// receipt, which will, for Opal; the banjo's new head, and Wendell's pie; Jed, who is watching it; and, with the schedule
// read, the way down. The scene starts it only when Ranger is at `over-room` and Joe is on the chair (and alone).
// ======================================================================================================
export const ventTree = (h = {}) => {
  const up = async (g) => { if (h.receiptUp) await h.receiptUp(g); g.flag("office.receiptUp", true); return "receiptGot"; };
  return {
    id: "vent",
    start: (g) => (is(g, "office.metAtVent") ? "talk" : "meet"),
    nodes: {
      meet: { say: ["office.vent.meet.1", "office.vent.meet.ranger", "office.vent.meet.joe"], then: (g) => { g.flag("office.metAtVent", true); return "talk"; } },
      talk: {
        options: [
          // #18: the banjo, and why; then the receipt, up through the slats
          { id: "banjo", line: "office.vent.opt.banjo", when: (g) => !is(g, "office.banjoBack") && !is(g, "office.receiptUp"),
            say: { 1: ["office.vent.banjo.1", "office.vent.banjo.ranger", "office.vent.banjo.joe"], more: ["office.vent.banjo.ranger", "office.vent.banjo.joe"] }, set: "office.planned" },
          { id: "receipt", line: "office.vent.opt.receipt", when: (g) => is(g, "office.planned") && g.has("receipt") && !is(g, "office.receiptUp"),
            then: (g) => (is(g, "office.sawProperty") ? "receiptKnown" : "receiptTell") },
          { id: "seenbanjo", line: "office.vent.opt.seenbanjo", when: (g) => is(g, "office.sawProperty") && !is(g, "office.banjoBack"),
            say: ["office.vent.seenbanjo.ranger", "office.vent.seenbanjo.joe"] },
          // #19: a pie, and who is watching it
          { id: "eat", line: "office.vent.opt.eat", when: (g) => is(g, "office.sawBreak") && !is(g, "office.pieEaten"),
            say: ["office.vent.eat.ranger", "office.vent.eat.joe"], then: (g) => (is(g, "office.jedGone") ? null : "jed") },
          { id: "head", line: "office.vent.opt.head", when: (g) => is(g, "office.banjoBack") && !is(g, "office.tinClean") && !g.has("pietin"),
            say: ["office.vent.head.1"], then: (g) => (is(g, "office.sawBreak") ? "headKnown" : "headLook") },
          { id: "jed", line: "office.vent.opt.jed", when: (g) => is(g, "office.jedTold") && !is(g, "office.jedGone"),
            say: ["office.vent.jedplan.ranger", "office.vent.jedplan.joe.1", "office.vent.jedplan.joe.2"] },
          { id: "trade", line: "office.vent.opt.trade", once: true, when: (g) => is(g, "office.pieEaten"), say: ["office.vent.trade.ranger", "office.vent.trade.joe"] },
          // #20: the way down, once the schedule is read
          { id: "down", line: "office.vent.opt.down", when: (g) => is(g, "office.schedule"), say: ["office.vent.down.ranger", "office.vent.down.joe.1", "office.vent.down.joe.2"] },
          // and the two of them
          { id: "promise", line: "office.vent.opt.promise", once: true, say: ["office.vent.promise.ranger", "office.vent.promise.joe"] },
          { id: "jolene", line: "office.vent.opt.jolene", say: { 1: ["office.vent.jolene.ranger", "office.vent.jolene.joe"], more: ["office.vent.jolene.2.ranger", "office.vent.jolene.2.joe"] } },
          { id: "bye", line: "office.vent.opt.bye", say: ["office.vent.bye.ranger"], then: "exit" },
        ],
      },
      receiptTell: { say: ["office.vent.receipt.1", "office.vent.receipt.ranger", "office.vent.receipt.joe", "office.vent.receipt.up"], then: up },
      receiptKnown: { say: ["office.vent.receipt.1", "office.vent.receipt.known.ranger", "office.vent.receipt.known.joe", "office.vent.receipt.up"], then: up },
      receiptGot: { say: ["office.vent.receipt.got"], then: "talk" },
      jed: { say: ["office.vent.jed.ranger", "office.vent.jed.joe.1", "office.vent.jed.joe.2"], then: (g) => { g.flag("office.jedTold", true); return "talk"; } },
      headKnown: { say: ["office.vent.head.known.ranger", "office.vent.head.known.joe"], then: "talk" },
      headLook: { say: ["office.vent.head.look.ranger", "office.vent.head.look.joe"], then: "talk" },
    },
  };
};

/** What the two of them say to each other outside the tree: the scene's `talk` when Ranger has dropped into the room (and
    the exchanges a script can say when Ranger, at the grille, has a word with Joe on his chair: ventTalk.ranger.grandpajoe).
    In the engine's form: a list of line ids, or { when, say }; what has not been heard comes first. */
export const ventTalk = {
  ranger: {
    grandpajoe: [
      ["office.vent.r.1", "office.vent.r.1.joe"],
      { when: (g) => is(g, "office.acOff"), say: ["office.vent.r.2", "office.vent.r.2.joe"] },
      ["office.vent.r.3", "office.vent.r.3.joe"],
      { when: (g) => is(g, "office.banjoBack") && !is(g, "office.mended"), say: ["office.vent.r.4", "office.vent.r.4.joe"] },
      { when: (g) => is(g, "office.schedule"), say: ["office.vent.r.5", "office.vent.r.5.joe"] },
    ],
  },
  grandpajoe: {
    ranger: [
      ["office.room.talk.joe.1a", "office.room.talk.joe.1b", "office.room.talk.joe.1c"],
      ["office.room.talk.joe.2a", "office.room.talk.joe.2b", "office.room.talk.joe.2c"],
    ],
  },
};

// ======================================================================================================
// opalTree: #18's end. Opal of Property & Effects, at the door of the Comfortable Room with the banjo, and two old-timers.
// "Forty-one statements of nothing, Joe Hollis." (the one time his surname is said). Then a few words, as many as he
// likes, and she goes, and locks the door behind her, gently. Plants stage two: her keys, the Director's sandal.
// ======================================================================================================
export const opalTree = (h = {}) => ({
  id: "opal",
  start: (g) => (is(g, "office.banjoBack") ? "chat" : "open"),
  nodes: {
    open: { say: ["office.opal.1", "office.opal.2", "office.opal.3", "office.opal.4", "office.opal.5"],
      then: async (g) => { if (h.sign) await h.sign(g); return "signed"; } },
    signed: { say: ["office.opal.6", "office.opal.7", "office.opal.8", "office.opal.9", "office.opal.10"],
      then: async (g) => { if (h.banjo) await h.banjo(g); g.flag("office.banjoBack", true); return "returned"; } },
    returned: { say: ["office.opal.11"], then: (g) => (rangerOver(g) ? "nod" : "chat") },
    nod: { say: ["office.opal.vent"], then: "chat" },                                   // two eyes in the room's vent: she looks up
    chat: {
      options: [
        { id: "damage", line: "office.opal.opt.damage", once: true, say: ["office.opal.damage.1", "office.opal.damage.2"] },
        { id: "jed", line: "office.opal.opt.jed", once: true, say: ["office.opal.jed.1", "office.opal.jed.2"] },
        { id: "sandal", line: "office.opal.opt.sandal", once: true, say: ["office.opal.sandal.1", "office.opal.sandal.2", "office.opal.sandal.3"] },
        { id: "lamp", line: "office.opal.opt.lamp", once: true, when: (g) => is(g, "office.lamplighter"), say: ["office.opal.lamp.1", "office.opal.lamp.2"] },
        { id: "door", line: "office.opal.opt.door", once: true, say: ["office.opal.door.1", "office.opal.door.2", "office.opal.door.3"] },
        { id: "thanks", line: "office.opal.opt.thanks", say: ["office.opal.thanks"], then: async (g) => { if (h.leave) await h.leave(g); return "gone"; } },
      ],
    },
    gone: { say: ["office.opal.lock"], then: async (g) => { if (h.gone) await h.gone(g); return "exit"; } },
  },
});

// ======================================================================================================
// intercomTree: #19's first half. Grandpa Joe, alone, at the intercom: DISPATCH. PRESS TO TALK. Houston answers. As
// himself he gets nothing (he is not Jed). He will not lie; he does not have to: he asks, nicely, on someone else's
// behalf, and Jed's cheeseburger is at the front desk at last. (Offered once the banjo is back and Ranger has told him Jed
// is sitting at the pie.)
// ======================================================================================================
export const intercomTree = (h = {}) => ({
  id: "intercom",
  start: "buzz",
  nodes: {
    buzz: { then: async (g) => { if (h.press) await h.press(g); return "press"; } },
    press: { say: ["office.intercom.press"], then: "talk" },
    talk: {
      options: [
        { id: "joe", line: "office.intercom.opt.joe", say: { 1: ["office.intercom.joe.1"], 2: ["office.intercom.joe.2"], more: ["office.intercom.joe.3"] } },
        { id: "name", line: "office.intercom.opt.name", once: true, when: (g) => g.asked("intercom/joe") > 0, say: ["office.intercom.name.1", "office.intercom.name.2"] },
        { id: "out", line: "office.intercom.opt.out", say: ["office.intercom.out"] },
        { id: "air", line: "office.intercom.opt.air", when: (g) => is(g, "office.acOff"), say: ["office.intercom.air.1", "office.intercom.air.2"] },
        { id: "burger", line: "office.intercom.opt.burger", say: { 1: ["office.intercom.burger.1"], more: ["office.intercom.burger.2"] } },
        // the lever: on Jed's behalf, and true (Jed said so himself, in the limousine)
        { id: "behalf", line: "office.intercom.opt.behalf", when: (g) => is(g, "office.banjoBack") && is(g, "office.jedTold") && !is(g, "office.jedGone"),
          say: ["office.intercom.behalf.1", "office.intercom.behalf.2"], do: h.burger, then: (g) => { g.flag("office.jedGone", true); return "behalf"; } },
        { id: "howjed", line: "office.intercom.opt.howjed", once: true, when: (g) => is(g, "office.jedGone"), say: ["office.intercom.howjed"] },
        { id: "lamp", line: "office.intercom.opt.lamp", when: (g) => is(g, "office.lamplighter"), say: ["office.intercom.lamp"] },
        { id: "b7", line: "office.intercom.opt.b7", when: (g) => is(g, "office.schedule"), say: ["office.intercom.b7.1", "office.intercom.b7.2", "office.intercom.b7.3"] },
        { id: "bye", line: "office.intercom.opt.bye", say: ["office.intercom.bye"], do: h.release, then: "exit" },
      ],
    },
    behalf: { say: ["office.intercom.behalf.3", "office.intercom.behalf.4"], then: "talk" },
  },
});

// ======================================================================================================
// ragTree: #20. The pie-tin banjo, the Last Stop Rag through every vent on every floor, and the suits at the door: "Sir.
// PLEASE, sir." He plays on through the talk. Before he has read the schedule he has nowhere he wants to go, and stops when
// asked nicely (he is a gentleman); after it, he asks for a room where he will not bother anybody, and there is only one.
// ======================================================================================================
export const ragTree = (h = {}) => {
  const medical = { id: "medical", line: "office.rag.opt.medical", say: { 1: ["office.rag.medical.1", "office.rag.medical.2", "office.rag.medical.3"], more: ["office.rag.medical.again"] } };
  const twice = { id: "twice", line: "office.rag.opt.twice", once: true, say: ["office.rag.twice.1", "office.rag.twice.2", "office.rag.twice.3"] };
  const home = { id: "home", line: "office.rag.opt.home", say: { 1: ["office.rag.home"], more: ["office.iv.leave.again.1"] } };
  const lamp = { id: "lamp", line: "office.rag.opt.lamp", once: true, say: ["office.rag.lamp.1", "office.rag.lamp.2", "office.rag.lamp.3", "office.rag.lamp.4", "office.rag.lamp.5"] };
  const somewhere = { id: "somewhere", line: "office.rag.opt.somewhere", say: ["office.rag.lever.1", "office.rag.lever.2"],
    then: async (g) => { if (h.louder) await h.louder(g); return "birthday"; } };
  const stop = { id: "stop", line: "office.rag.opt.stop", say: ["office.rag.stop.1", "office.rag.stop.2", "office.rag.stop.3"], do: h.stop, then: "exit" };
  return {
    id: "rag",
    start: "door",
    nodes: {
      door: { say: ["office.rag.door.1", "office.rag.door.2", "office.rag.door.3"], then: (g) => (is(g, "office.schedule") ? "know" : "early") },
      early: { options: [medical, twice, home, stop] },
      know: { options: [medical, twice, lamp, somewhere, home, stop] },
      birthday: { say: ["office.rag.lever.3", "office.rag.lever.4"], then: async (g) => { g.flag("office.down", true); if (h.down) await h.down(g); return "exit"; } },
    },
  };
};

// ======================================================================================================
// Now and then: what each place says by itself, a little at a time (a scene's script says one exchange every so often,
// the ones not heard yet first, as g.chat picks them; heard from a grille too, since the room's scripts run while it is
// looked down into). In the engine's form: a list of line ids, or { when, say }.
// ======================================================================================================
const jedThere = (g) => !is(g, "office.jedGone");
export const nowAndThen = {
  // Wendell on the door, to the gate (the second only before the raccoon is noted: office.trash is the scene's fact for it)
  "office-lot": [
    ["office.lot.wendell.idle.1"],
    { when: (g) => !is(g, "office.trash"), say: ["office.lot.wendell.idle.2"] },
  ],
  // the interview, as Ranger hears it from the grille while it goes on (the questionnaire repeats itself: that is the joke)
  "office-room": [
    { when: (g) => !is(g, "office.alone"), say: ["office.iv.sorry", "office.iv.m1", "office.iv.opt.m1.a", "office.iv.m1.a"] },
    { when: (g) => !is(g, "office.alone"), say: ["office.iv.sorry.3", "office.iv.m3", "office.iv.opt.m3.a", "office.iv.m3.a"] },
    { when: (g) => !is(g, "office.alone"), say: ["office.iv.sorry.2", "office.iv.m2", "office.iv.opt.m2.a", "office.iv.m2.a"] },
    { when: (g) => !is(g, "office.alone") && Number(g.flag("office.heat")) >= 77, say: ["office.room.merle.mop", "office.room.dale.tie"] },
  ],
  // Opal at her window, her back to the shelves
  "office-property": [["office.prop.opal.idle.1"], ["office.prop.opal.idle.2"], ["office.prop.opal.idle.3"], ["office.prop.opal.idle.4"]],
  // Jed in his chair, facing the pie; Floyd asleep on the couch (and g.think("suit4", "zzz", { loop: true }) the while)
  "office-breakroom": [
    { when: jedThere, say: ["office.jed.idle.1"] },
    { when: jedThere, say: ["office.jed.idle.2"] },
    { when: jedThere, say: ["office.jed.idle.3", "office.floyd.1"] },
    { when: jedThere, say: ["office.jed.idle.4", "office.jed.idle.5", "office.jed.idle.6"] },
    { when: jedThere, say: ["office.jed.idle.7"] },
    ["office.floyd.2"], ["office.floyd.3"], ["office.floyd.4"],
  ],
};

/** Houston on the speakers, now and then, with the moment each belongs to (await g.pa(id), in any scene of the building).
    The story's own announcements (office.pa.arrive, .pie, .raccoon, .air.*, .burger, .music, .down, .test) are said by
    the scripts at their moments: ids.md says which. */
export const paNowAndThen = [
  { id: "office.pa.fairweather" },
  { id: "office.pa.limo" },
  { id: "office.pa.plant" },
  { id: "office.pa.form7" },
  { id: "office.pa.peanuts", when: (g) => !is(g, "office.peanuts") },             // office.peanuts: the scene's fact, Ranger has his packet
  { id: "office.pa.peanuts.2", when: (g) => is(g, "office.peanuts") },
  { id: "office.pa.comfort", when: (g) => Number(g.flag("office.heat")) >= 77 },
];

/** Every tree, by name, for the tests. */
export const trees = { interviewTree, ventTree, opalTree, intercomTree, ragTree };

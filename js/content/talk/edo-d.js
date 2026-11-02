// The talks of Act Six's road on from the hills: Akashi, Himeji town, the foot of Mount Shosha and the women's hall (WRITE-21B:
// new in round twenty-one; briefs/WRITE-21.md, and the design, briefs/out/edo2-design.md, #35 to #38, "Mind The Fire", the
// cards). Plain data in the engine's format (docs/DESIGN.md, section 7, "Dialogue trees"), made as talk/edo-b.js makes them:
// every word is a line id (js/content/lines/edo-d.en.js). An option's `line` is said by the one it belongs to; its `say` is
// the reply (a list, or { 1, 2, more } by how many times it has been picked); `set` makes facts true; `do` is a script;
// `then` goes to a node, "back", "root" or "exit" (or is a function of the game giving one). WRITE-21A's trees are in
// talk/edo-c.js; the phase-B lead joins the halves.
//
// Each tree is a function of a `hooks` object, so that the scene hands in the scripts a branch needs:
//     import { fusaTree } from "../talk/edo-d.js";
//     ...  use: (g) => g.talk(fusaTree({ giveLadle, giveSlip, givePenny }))
// A hook that is not handed in is passed over (the talk still says every line and sets every fact).
//
// THE SON (sonTree, #38) speaks from the other end of a small door. His lines must go through it, with his portrait (the
// letterbox: docs/DESIGN.md, section 8). The engine does that for a whole talk held `{ through: "son" }`, but then every
// menu is HIS words (the Nevada letterbox's way). Here the menus are the family's (Mom first, each girl her own branch),
// so sonTree speaks every line itself, by its speaker: the Son's through the door (`g.through("son", id)`), everyone
// else's as `g.say`. The scene holds it plainly: `g.talk(sonTree(h))`. (If ENGINE-21 gives the engine a way to send one
// voice through a door while the menus stay the leads', the tree's `voice` helper below is the one place to change.)
//
// THE HOOKS, and what each must do. None of them says a line the tree says.
//   fusaTree (edo-akashi, #35: O-Fusa on the sand, in tears)
//     giveLadle(g)  the ladle into her hands: g.take("ladle") from whoever has it. After edo.akashi.fusa.back.1's option.
//     giveSlip(g)   her name slip to the one who gave the ladle back (Little Sister, as a rule): g.give("fusaslip", ...).
//     givePenny(g)  Little Sister's penny for luck: her `twopennies` become `lastpenny`. (The tree sets edo.ladleBack after.)
//   heitaTree, leaderTree, satoTree (edo-akashi): no hooks. heitaTree sets edo.crabClue (the clue: "Except for a crab.")
//                 and edo.tako (Big Sister's gloss is said once in the act: the scene's first pull reads it too);
//                 satoTree sets edo.riddle.
//   taneTree (edo-town, #36: O-Tane at her door)
//     kitchen(g)    she hands Mom her rice paddle, and her kitchen is Mom's for an hour (staging; the tree sets
//                   edo.kitchenLent before Big Sister's line about two kitchens).
//   kikuTree (edo-town, #36: O-Kiku at the school door, in her best, saying nothing)
//     goIn(g)       Little Sister takes her hand and the two of them go in, to the desks (`desk`); the teacher kneels.
//     comeOut(g)    after the lesson (the tree says edo.town.lesson.1 to .4 inside), out again to O-Tane at her door.
//                   (The tree says .5 to .7 and sets edo.kikuIn.)
//   shizuTree (edo-town, #36: O-Shizu)
//     drawWay(g)    she draws them the way on a scrap of practice paper (staging: the map's `shosha` shows from the fact
//                   edo.knowWay, which the tree sets).
//   tobeiTree (edo-town, #36: Tōbei on his stool)
//     sweet(g)      he gives Little Sister a sweet from the jar (staging: no item; she eats it).
//   umeTree (edo-shosha, #37: O-Ume by her hut)
//     slipNatsu(g)  O-Natsu's slip into O-Ume's hands: g.take("natsuslip"). (The tree sets edo.natsuGiven.)
//     slipFusa(g)   O-Fusa's slip the same: g.take("fusaslip"). (edo.fusaGiven.)
//   ryokaiTree, tomeTree, wifeTree, girlTree (edo-shosha): no hooks.
//   hallUmeTree, hallRyokaiTree (edo-hall: O-Ume kneeling by the door; Ryōkai's face at the lattice): no hooks.
//   sonTree (edo-hall, #38: the scene starts it when the small door first opens, and on any use of the door after)
//     sit(g)        Mom sits down on the mats (before "It's not a closet."): staging.
//     fade(g)       the sun goes: the bars of light climb and fade; the flashlight flickers (after his last line).
//     close(g)      the door shrinks to a coin, to a point, and is gone (after Big Sister's "Isaiah 49:15.").
//     done(g)       the scene's cue for "Mind The Fire" (the tree has said O-Ume's question and Mom's answer).
//     (The rice ball and the flashlight are the scene's uses of the door, with the lists HALL.riceball and HALL.flash.)
//
// THE FACTS. Set by the trees: edo.fusaMet, edo.ladleBack (#35, with the hooks), edo.heitaMet, edo.tako, edo.crabClue,
// edo.satoMet, edo.riddle; edo.taneMet, edo.kitchenLent, edo.taneBed, edo.kikuIn, edo.shizuThanked, edo.knowWay,
// edo.tobeiMet (#36); edo.umeGreeted, edo.riddle, edo.oumeMet, edo.natsuGiven, edo.fusaGiven, edo.listRead,
// edo.ryokaiMet, edo.tomeMet (#37); edo.sonHeard, edo.eatenAsked, edo.holdHands (#38). Set by the scenes, and read here:
// edo.waded, edo.crab, edo.ladleFree (#35); edo.riceballs (#36); edo.lockSeen, edo.earClean, edo.earHeld, edo.postHeld,
// edo.hallOpen (#37); edo.doorWide, edo.sonFed (#38); edo.nightDone (the night is over: the next day). And g.has(item).
//
// Besides the trees: the lists for the cards and cut-scenes (WALK, WALK2, NIGHT, STEP), each scene's beats (AKASHI, TOWN,
// SHOSHA, HALL), the kitchen's order (COOK), the lock's table (LOCK), the map's far lines (farLine), the hints (HINTS and
// hintFor), and `trees`, every tree by name, for the tests. S/work-21-writeB/ids.md says when each line is said.

const who = (g) => g.store.data.active;
const is = (g, fact) => !!g.flag(fact);
const run = async (g, hook) => { if (typeof hook === "function") await hook(g); };
/** Is the thing in this lead's pockets (any lead, not only the active one)? */
const holds = (g, lead, item) => (((g.store && g.store.data && g.store.data.inventory) || {})[lead] || []).includes(item);

// ======================================================================================================
// THE CARDS AND CUT-SCENES (their scripts are phase B's; the lines are here in order)
// ======================================================================================================
/** The walk card, edited: "Three days later" / "Akashi" (round twenty's ids: the second is edited in edo-b.en.js), Little
    Sister's line under it (as built), and a line at each of the three road pictures as the portraits pass (ENGINE-21's
    journey stops). Suma may say both its lines, if the stop takes a list; the first alone is enough. */
export const WALK = {
  card: ["edo.walk.card", "edo.walk.card.2"],
  under: ["edo.walk.lilsis"],
  stops: { koriyama: ["edo.walk.stop.koriyama"], suma: ["edo.walk.stop.suma", "edo.walk.stop.suma.2"], maiko: ["edo.walk.stop.maiko"] },
};
/** The card "The next day" / "Himeji" (the beat edo.walk2): Akashi to the town, at `east`. */
export const WALK2 = { card: ["edo.walk2.card", "edo.walk2.card.2"] };
/** "Mind The Fire" (the beat edo.night): the title; O-Ume's lantern; the fields and the frogs; Tōbei at the shut gate (the
    clappers struck after .3, and answered from far off before .4); O-Tane's door; the dark; the card, then the castle. */
export const NIGHT = {
  title: "edo.night.title",
  lantern: ["edo.night.ume.1", "edo.night.ume.2", "edo.night.ume.3"],
  fields: ["edo.night.field.1", "edo.night.field.2", "edo.night.field.3"],
  gate: ["edo.night.tobei.1", "edo.night.tobei.2", "edo.night.tobei.3"],
  passed: ["edo.night.tobei.4", "edo.night.tobei.5", "edo.night.tobei.6", "edo.night.tobei.7"],
  door: ["edo.night.tane.1", "edo.night.tane.2"],
  dark: ["edo.night.dark.1", "edo.night.dark.2", "edo.night.dark.3"],
  card: "edo.night.card",
};
/** "Hold Hands" (edo-step.js), as round twenty's STEP (talk/edo-b.js) with Little Sister's new line first: she takes both
    their hands before Mom's "Places, girls." (edo.step.0; it may go after edo.step.1 instead). Mom's prayer is edited in
    place (edo.step.pray.1, edo-b.en.js). */
export const STEP = {
  title: "edo.step.title",
  places: ["edo.step.0", "edo.step.1", "edo.step.2", "edo.step.3"],
  prayer: ["edo.step.pray.1", "edo.step.pray.2", "edo.step.pray.3"],
  goodbyes: ["edo.step.4", "edo.step.5", "edo.step.6", "edo.step.7"],
  poem: ["edo.step.poem.1", "edo.step.poem.2", "edo.step.poem.3", "edo.step.poem.4"],
  card: "edo.step.card",
};

// ======================================================================================================
// EACH SCENE'S BEATS (what the scene says at a moment, in order)
// ======================================================================================================
const byLead = (base) => ({ mom: `${base}.mom`, bigsis: `${base}.bigsis`, lilsis: `${base}.lilsis` });
/** edo-akashi (#35). `arrive` once at `road`. `wade`: Little Sister's use of the shallows or the ladle (edo.waded); the
    others' uses are refusals. `pull`: her use of the ladle while the octopus has it; .2 (Heita's clue) and .3 (the
    gloss, unless edo.tako) only the first time, and they set edo.crabClue and edo.tako. `crab`: Mom's use of the rocks
    after edo.crabClue (edo.crab; the crab into her pockets); `crabAgain` after. `swap`: Little Sister's crab on the ladle
    (the crab gone, the ladle hers, edo.ladleFree; Heita lifts the octopus at .4). The road: `east` refuses always;
    `west` refuses until edo.ladleBack, then `westGo` and the card (WALK2). */
export const AKASHI = {
  arrive: ["edo.akashi.arrive.1", "edo.akashi.arrive.2", "edo.akashi.arrive.3"],
  wade: ["edo.akashi.wade.1", "edo.akashi.wade.2", "edo.akashi.wade.3"],
  pull: ["edo.akashi.pull.1", "edo.akashi.pull.2", "edo.akashi.pull.3"],
  crab: ["edo.akashi.rocks.crab.1", "edo.akashi.rocks.crab.2", "edo.akashi.rocks.crab.3"],
  crabAgain: "edo.akashi.rocks.again.mom",
  swap: ["edo.akashi.swap.1", "edo.akashi.swap.2", "edo.akashi.swap.3", "edo.akashi.swap.4"],
  pots: "edo.akashi.pots.heita",                    // after Little Sister's look at the pots, the first time (Heita, from his boat)
  east: byLead("edo.akashi.east"),
  west: byLead("edo.akashi.west"),
  westGo: "edo.akashi.west.go",
};
/** edo-town (#36). `arrive` once at `east`. The well's look by Little Sister is answered by Mom (`well`). `north` refuses
    before the night (`northAfter` once supper is made and the way known); `highway` (east) always refuses: its use lines
    are edo.town.highway.use.<who>. */
export const TOWN = {
  arrive: ["edo.town.arrive.1", "edo.town.arrive.2", "edo.town.arrive.3"],
  well: ["edo.town.well.lilsis", "edo.town.well.lilsis.2"],
  cotton: ["edo.town.cottonoffice.use.bigsis", "edo.town.cottonoffice.use.bigsis.2", "edo.town.cottonoffice.use.bigsis.3", "edo.town.cottonoffice.use.bigsis.4"],
  north: byLead("edo.town.north"),
  northAfter: "edo.town.north.after.mom",
  pupils: ["edo.town.pupil1.say", "edo.town.pupil2.say"],      // now and then, while Little Sister is at a desk (the school's life)
};
/** O-Tane's kitchen (#36, Mom's for an hour, edo.kitchenLent): five steps in order, each a use by Mom (`water`: the
    bucket or the well; `salt`: the salt jar; `rice`: the rice pot; `pickle`: the pickle tub; `cloth`: the cloth). A step
    out of order is a funny line (`early`, by the first missing step), never a failure. The plum jar is a free extra once
    the rice is shaped (`plum`). The last step gives Mom the `riceball` and sets edo.riceballs; the cloth's look becomes
    its `.bundle`. Big Sister's and Little Sister's uses of the kitchen's things while it is Mom's: `girls`. */
export const COOK = {
  order: ["water", "salt", "rice", "pickle", "cloth"],
  done: { water: ["edo.town.cook.water", "edo.town.cook.water.2"], salt: ["edo.town.cook.salt"], rice: ["edo.town.cook.rice", "edo.town.cook.rice.2"],
    pickle: ["edo.town.cook.pickle"], cloth: ["edo.town.cook.cloth", "edo.town.cook.cloth.2"] },
  early: { "salt/water": "edo.town.cook.nowater.salt", "rice/water": "edo.town.cook.nowater.rice", "rice/salt": "edo.town.cook.nosalt.rice",
    "pickle/rice": "edo.town.cook.norice.pickle", "cloth/rice": "edo.town.cook.norice.cloth", "cloth/pickle": "edo.town.cook.nopickle.cloth",
    "pickle/water": "edo.town.cook.norice.pickle", "pickle/salt": "edo.town.cook.norice.pickle", "cloth/water": "edo.town.cook.norice.cloth",
    "cloth/salt": "edo.town.cook.norice.cloth" },
  plum: "edo.town.cook.plum",
  noPlum: "edo.town.cook.noplum",                 // the plum jar before the rice is shaped
  again: "edo.town.cook.again",                   // a step already done, before the end
  after: "edo.town.cook.done",                    // anything in the kitchen once the cloth is tied
  girls: { bigsis: "edo.town.cook.bigsis", lilsis: "edo.town.cook.lilsis" },
};
/** What Mom says at a step of the kitchen, given the steps done so far (a Set or list of COOK.order names). */
export function cookLines(doneSteps, step) {
  const done = new Set(doneSteps || []);
  if (done.has("cloth")) return [COOK.after];
  if (step === "plum") return [done.has("rice") ? COOK.plum : COOK.noPlum];
  if (done.has(step)) return [COOK.again];
  for (const need of COOK.order) {
    if (need === step) break;
    if (!done.has(need)) return [COOK.early[`${step}/${need}`] || COOK.early[`${step}/rice`] || "edo.town.cook.norice.cloth"];
  }
  return COOK.done[step];
}
/** edo-shosha (#37). `arrive` once at `road` (the women argue; O-Ume settles it). The east path (or the mountain): the
    first try by any of them is Ryōkai's `climb` and then hers (`first`); Mom's own first try is the psalm (`psalm`, said
    once in the act, whenever she first tries), and after it the lines edo.shosha.pathup.use.<who>. `stone`: Ryōkai says
    what it says, the first time it is used. `list`: Big Sister's note read against the riddle (edo.listRead), however it
    is reached (her umeTree option; her note on the lock, the heap of combs or O-Ume), and `listAgain` after. `open`: the
    doors open (after the close-up's LOCK.open): the women in first, the slips up, a rice ball and a coin for O-Ume, and
    the sun low; `slips`: if a slip was not given before, the one who carries it says hers before `open.2`. */
export const SHOSHA = {
  arrive: ["edo.shosha.arrive.1", "edo.shosha.arrive.2", "edo.shosha.arrive.3"],
  climb: ["edo.shosha.climb.1", "edo.shosha.climb.2"],
  first: { mom: ["edo.shosha.psalm.1", "edo.shosha.psalm.2", "edo.shosha.psalm.3", "edo.shosha.psalm.4", "edo.shosha.psalm.5"],
    bigsis: ["edo.shosha.climb.bigsis"], lilsis: ["edo.shosha.climb.lilsis", "edo.shosha.climb.lilsis.2"] },
  psalm: ["edo.shosha.psalm.1", "edo.shosha.psalm.2", "edo.shosha.psalm.3", "edo.shosha.psalm.4", "edo.shosha.psalm.5"],
  stone: "edo.shosha.stone.ryokai",
  list: ["edo.shosha.list.1", "edo.shosha.list.2", "edo.shosha.list.3", "edo.shosha.list.4", "edo.shosha.list.5", "edo.shosha.list.6", "edo.shosha.list.7"],
  listAgain: "edo.shosha.list.again.bigsis",
  combsRead: "edo.shosha.combs.read.bigsis",            // Big Sister's use of the heap after edo.listRead
  open: ["edo.shosha.open.1", "edo.shosha.open.2", "edo.shosha.open.3", "edo.shosha.open.4", "edo.shosha.open.5", "edo.shosha.open.6", "edo.shosha.open.7", "edo.shosha.open.8"],
  slips: { natsuslip: "edo.shosha.slip.natsu", fusaslip: "edo.shosha.slip.fusa" },
  after: { tome: "edo.shosha.tome.after", wife: "edo.shosha.wife.after", girl: "edo.shosha.girl.after" },
};
/** edo-hall (#38). `enter` once (O-Ume; Grandmother Tome going home). `kannon`: the first use of the cabinet by anyone.
    `flash`: Little Sister's flashlight on the hum (or the door) once the small door is open: the door grows to a hand
    (edo.doorWide). `riceball`: Mom's rice ball into the door a hand wide (g.send("riceball", { to: "son" }) between .1
    and .2; edo.sonFed after .5); `riceballSmall` is her try while it is only a coin wide. The Son's lines in these lists go
    through the door (sonVoice). */
export const HALL = {
  enter: ["edo.hall.enter.1", "edo.hall.enter.2"],
  kannon: ["edo.hall.kannon.1", "edo.hall.kannon.2", "edo.hall.kannon.3", "edo.hall.kannon.4"],
  flash: ["edo.hall.flash.1", "edo.hall.flash.2"],
  riceball: ["edo.hall.riceball.1", "edo.hall.riceball.2", "edo.hall.riceball.3", "edo.hall.riceball.4", "edo.hall.riceball.5"],
  riceballSmall: "edo.hall.door.with.riceball.mom",
};

// ======================================================================================================
// THE LOCK (edo-lock, the close-up: #37's three tricks). A look is edo.lock.<thing>[.<state>].<who>; a use with nothing
// edo.lock.<thing>[.<state>].use.<who>; a use with a carried thing edo.lock.<thing>[.<state>].with.<item>.<who>[.1, .2],
// else the thing's own fallback edo.lock.with.<item>.<who>. The states: ear `clean` (edo.earClean); wave `slid` and post
// `showing` (while edo.earHeld); post `turned` and back `slits` (while edo.postHeld); bolt `out` (edo.hallOpen). The
// earhole takes the ear's lines for things used on it.
// ======================================================================================================
export const LOCK = {
  first: "edo.lock.first",                     // the first time the close-up opens (edo.lockSeen): Grandmother Tome, from the bench
  party: "edo.lock.party",                     // the first time one of the three things is handed to another of them
  give: { kanzashi: "edo.lock.give.kanzashi", mon: "edo.lock.give.mon", comb: "edo.lock.give.comb" },   // to its right one: the giver says it
  rightHands: { kanzashi: "lilsis", mon: "mom", comb: "bigsis" },
  letgo: byLead("edo.lock.letgo"),             // stepping back with a part held: everything springs back (by whoever steps back)
  open: ["edo.lock.open.1", "edo.lock.open.2", "edo.lock.open.3", "edo.lock.open.4"],      // the comb home: the chirp after .1
  rabbitMom: ["edo.lock.rabbit.use.mom", "edo.lock.rabbit.use.mom.2"],
};
/** The state word for a thing of the lock, from the facts. */
export function lockState(g, thing) {
  if (thing === "ear" || thing === "earhole") return is(g, "edo.earClean") && thing === "ear" ? "clean" : null;
  if (thing === "wave") return is(g, "edo.earHeld") ? "slid" : null;
  if (thing === "post") return is(g, "edo.postHeld") ? "turned" : is(g, "edo.earHeld") ? "showing" : null;
  if (thing === "back") return is(g, "edo.postHeld") ? "slits" : null;
  if (thing === "bolt") return is(g, "edo.hallOpen") ? "out" : null;
  return null;
}
/** The line ids for a use of the lock's `thing` by `lead`, with `item` or with nothing; `lines` is g.lines (to choose the
    first id that exists, from the most particular to the most general). Big Sister's note before edo.listRead is the
    list's trigger (the scene then says SHOSHA.list and sets edo.listRead); after it, her short form. Success lines come back as their pair
    (.1 and .2): the scene acts between or after them (the ear held, the post held, the lock opening). */
export function lockLines(g, lines, thing, lead, item = null) {
  const part = thing === "earhole" && item ? "ear" : thing;
  const st = lockState(g, part);
  const base = `edo.lock.${part}${st ? "." + st : ""}`;
  const pick = (...ids) => { for (const id of ids) { if (Array.isArray(id)) { if (id.every((x) => lines[x])) return id; } else if (lines[id]) return [id]; } return null; };
  if (!item) return pick(`${base}.use.${lead}`, `edo.lock.${part}.use.${lead}`) || [];
  if (item === "note" && is(g, "edo.listRead")) return pick(`edo.lock.with.note.read.${lead}`, `edo.lock.with.note.${lead}`) || [];
  return pick([`${base}.with.${item}.${lead}.1`, `${base}.with.${item}.${lead}.2`], `${base}.with.${item}.${lead}`,
    `edo.lock.${part}.with.${item}.${lead}`, `edo.lock.with.${item}.${lead}`) || [];
}

// ======================================================================================================
// THE MAP: the far line for a place of another leg, by the family's leg (maps.js `far` as a function of the game:
// `far: (g) => farLine(g, "yui")`, with the leg the act's own fact or the map's: ENGINE-21 says which). Legs: 1 Yui, 2 Osaka,
// 3 the hills, 4 Akashi, 5 Himeji and Shosha. Falls back to round twenty's one line for the place.
// ======================================================================================================
export const FAR = {
  yui: { 2: "edo.map.far.yui.2", 3: "edo.map.far.yui.3", 4: "edo.map.far.yui.4", 5: "edo.map.far.yui.5" },
  osaka: { 3: "edo.map.far.osaka.3", 4: "edo.map.far.osaka.4", 5: "edo.map.far.osaka.5" },
  hills: { 2: "edo.map.far.hills.2", 4: "edo.map.far.hills.4", 5: "edo.map.far.hills.5" },
  akashi: { 3: "edo.map.far.akashi.3", 5: "edo.map.far.akashi.5" },
  himeji: { 2: "edo.map.far.himeji.2", 3: "edo.map.far.himeji.3", 4: "edo.map.far.himeji.4" },
};
export function farLine(place, leg) { return (FAR[place] && FAR[place][leg]) || `edo.map.far.${place}`; }
/** Shosha on the map, inside the fifth leg: the walk there (`way`); not before supper is made (`nosupper`); not back to
    the town while the sun is setting there (`stay`); and, the next day, not back at all (`done`). */
export const SHOSHA_MAP = { way: "edo.map.shosha.way", nosupper: "edo.map.shosha.nosupper", stay: "edo.map.shosha.stay", done: "edo.map.shosha.done" };

// ======================================================================================================
// fusaTree: #35, The Ladle. O-Fusa, nine, an Awa pilgrim in tears: her ladle went into the sea as she waded, and a
// pilgrim with no ladle is fed nowhere. Each lead her own way in; Little Sister's is the lever (boots). The ladle back:
// the slip for the women's hall at Shosha, and a penny for luck ("He looks hungry.").
// ======================================================================================================
export const fusaTree = (h = {}) => {
  const back = async (g) => { await run(g, h.giveLadle); return "given"; };
  return {
    id: "fusa",
    start: (g) => (is(g, "edo.ladleBack") ? "after" : is(g, "edo.fusaMet") ? "talk" : "meet"),
    nodes: {
      meet: { say: ["edo.akashi.fusa.meet.1", "edo.akashi.fusa.meet.2"], then: (g) => { g.flag("edo.fusaMet", true); return "talk"; } },
      talk: {
        options: [
          { id: "help", line: "edo.akashi.fusa.opt.lilsis", once: true, when: (g) => who(g) === "lilsis" && !g.has("ladle"),
            say: ["edo.akashi.fusa.lilsis.1", "edo.akashi.fusa.lilsis.2", "edo.akashi.fusa.lilsis.3"] },
          { id: "where", clue: true, line: "edo.akashi.fusa.opt.where", when: (g) => who(g) === "lilsis" && !is(g, "edo.ladleFree"), say: ["edo.akashi.fusa.where.1"] },
          { id: "mom", line: "edo.akashi.fusa.opt.mom", once: true, when: (g) => who(g) === "mom", say: ["edo.akashi.fusa.mom.1", "edo.akashi.fusa.mom.2", "edo.akashi.fusa.mom.3"] },
          { id: "bigsis", line: "edo.akashi.fusa.opt.bigsis", once: true, when: (g) => who(g) === "bigsis", say: ["edo.akashi.fusa.bigsis.1", "edo.akashi.fusa.bigsis.2", "edo.akashi.fusa.bigsis.3"] },
          // the ladle back, by whoever has it
          { id: "back", line: "edo.akashi.fusa.opt.back", when: (g) => who(g) === "lilsis" && g.has("ladle"), say: ["edo.akashi.fusa.back.1"], then: back },
          { id: "backMom", line: "edo.akashi.fusa.opt.back.mom", when: (g) => who(g) === "mom" && g.has("ladle"), say: ["edo.akashi.fusa.back.1"], then: back },
          { id: "backBig", line: "edo.akashi.fusa.opt.back.bigsis", when: (g) => who(g) === "bigsis" && g.has("ladle"), say: ["edo.akashi.fusa.back.1"], then: back },
          { id: "byeLil", line: "edo.akashi.fusa.bye.lilsis", when: (g) => who(g) === "lilsis", say: ["edo.akashi.fusa.bye"], then: "exit" },
          { id: "bye", line: "edo.akashi.fusa.bye.mom", when: (g) => who(g) !== "lilsis", say: ["edo.akashi.fusa.bye.2"], then: "exit" },
        ],
      },
      // the slip for Shosha, and the penny for luck (Little Sister says .4 and .6 whoever gave the ladle: she is there)
      given: { say: ["edo.akashi.fusa.back.2", "edo.akashi.fusa.back.3"], then: async (g) => { await run(g, h.giveSlip); return "penny"; } },
      penny: { say: ["edo.akashi.fusa.back.4"], then: async (g) => { await run(g, h.givePenny); return "lucky"; } },
      lucky: { say: ["edo.akashi.fusa.back.5", "edo.akashi.fusa.back.6"], then: (g) => { g.flag("edo.ladleBack", true); return "exit"; } },
      after: { say: ["edo.akashi.fusa.bye"], then: "exit" },
    },
  };
};

// ======================================================================================================
// leaderTree: O-Fusa's group's leader, with the banner, counting heads (thirty, and one ladle in the sea).
// ======================================================================================================
export const leaderTree = (h = {}) => ({
  id: "leader",
  start: (g) => (is(g, "edo.ladleBack") ? "after" : "count"),
  nodes: {
    count: {
      say: ["edo.akashi.leader.count"],
      options: [
        { id: "wait", line: "edo.akashi.leader.opt.wait", once: true, when: (g) => who(g) === "mom", say: ["edo.akashi.leader.wait.1"] },
        { id: "count", line: "edo.akashi.leader.opt.count", once: true, when: (g) => who(g) === "bigsis", say: ["edo.akashi.leader.count.1"] },
        { id: "flag", line: "edo.akashi.leader.opt.flag", once: true, when: (g) => who(g) === "lilsis", say: ["edo.akashi.leader.flag.1", "edo.akashi.leader.flag.2"] },
        { id: "bye", line: "edo.akashi.leader.opt.bye", say: ["edo.akashi.leader.bye"], then: "exit" },
      ],
    },
    after: { say: ["edo.akashi.leader.after"], then: "exit" },
  },
});

// ======================================================================================================
// heitaTree: old Heita, octopus fisherman: few words, all of them about octopus. The clue (a tako lets go of nothing,
// except for a crab) for any of the three, once the ladle has a passenger; the pots; whose octopus. Big Sister glosses
// "tako" the first time anybody hears it (edo.tako).
// ======================================================================================================
export const heitaTree = (h = {}) => {
  const clue = { say: { 1: ["edo.akashi.heita.letgo.1"], more: ["edo.akashi.heita.letgo.again"] }, set: "edo.crabClue" };
  return {
    id: "heita",
    start: (g) => (is(g, "edo.ladleFree") ? "after" : is(g, "edo.heitaMet") ? "talk" : "meet"),
    nodes: {
      meet: { say: ["edo.akashi.heita.meet.1"], then: (g) => { g.flag("edo.heitaMet", true); return is(g, "edo.tako") ? "talk" : "gloss"; } },
      gloss: { say: ["edo.akashi.heita.meet.2"], then: (g) => { g.flag("edo.tako", true); return "talk"; } },
      talk: {
        options: [
          { id: "ladle", line: "edo.akashi.heita.opt.ladle", once: true, when: (g) => who(g) === "mom", say: ["edo.akashi.heita.ladle.1"] },
          { id: "letgo", clue: true, line: "edo.akashi.heita.opt.letgo", when: (g) => who(g) === "mom" && is(g, "edo.waded"), ...clue },
          { id: "letgoBig", clue: true, line: "edo.akashi.heita.opt.letgo.bigsis", when: (g) => who(g) === "bigsis" && is(g, "edo.waded"), ...clue },
          { id: "letgoLil", clue: true, line: "edo.akashi.heita.opt.letgo.lilsis", when: (g) => who(g) === "lilsis" && is(g, "edo.waded"), ...clue },
          { id: "pots", line: "edo.akashi.heita.opt.pots", once: true, when: (g) => who(g) === "bigsis", say: ["edo.akashi.heita.pots.1"] },
          { id: "yours", line: "edo.akashi.heita.opt.yours", once: true, when: (g) => who(g) === "lilsis", say: ["edo.akashi.heita.yours.1"] },
          { id: "crab", clue: true, line: "edo.akashi.heita.opt.crab", when: (g) => who(g) === "lilsis" && is(g, "edo.crabClue") && !is(g, "edo.crab"), say: ["edo.akashi.heita.crab.1"] },
          { id: "byeLil", line: "edo.akashi.heita.bye.lilsis", when: (g) => who(g) === "lilsis", say: ["edo.akashi.heita.bye"], then: "exit" },
          { id: "bye", line: "edo.akashi.heita.bye.mom", when: (g) => who(g) !== "lilsis", say: ["edo.akashi.heita.bye"], then: "exit" },
        ],
      },
      after: { say: ["edo.akashi.heita.after"], then: "exit" },
    },
  };
};

// ======================================================================================================
// satoTree: O-Sato and her sister-in-law, Harima women slipping away east to Ise with their ladles ("We're at the
// market."): the news from Shosha for Mom or Big Sister (the hall still shut; O-Ume's rice balls; her husband the
// shipwright; the riddle): edo.riddle. A clue: asked again, the short form keeps the riddle.
// ======================================================================================================
export const satoTree = (h = {}) => {
  const news = { 1: ["edo.akashi.sato.shosha.1", "edo.akashi.sato.shosha.2", "edo.akashi.sato.shosha.3", "edo.akashi.sato.shosha.4", "edo.akashi.sato.shosha.5", "edo.akashi.sato.shosha.6"],
    more: ["edo.akashi.sato.shosha.again"] };
  return {
    id: "sato",
    start: (g) => (is(g, "edo.satoMet") ? "talk" : "meet"),
    nodes: {
      meet: { say: ["edo.akashi.sato.meet.1", "edo.akashi.sato.meet.2"], then: (g) => { g.flag("edo.satoMet", true); return "talk"; } },
      talk: {
        options: [
          { id: "where", line: "edo.akashi.sato.opt.where", once: true, when: (g) => who(g) === "mom", say: ["edo.akashi.sato.where.1", "edo.akashi.sato.where.2"] },
          { id: "shosha", clue: true, line: "edo.akashi.sato.opt.shosha", when: (g) => who(g) === "mom", say: news, set: "edo.riddle" },
          { id: "shoshaBig", clue: true, line: "edo.akashi.sato.opt.shosha.bigsis", when: (g) => who(g) === "bigsis", say: news, set: "edo.riddle" },
          { id: "ladle", line: "edo.akashi.sato.opt.ladle", once: true, when: (g) => who(g) === "lilsis", say: ["edo.akashi.sato.ladle.1", "edo.akashi.sato.ladle.2"] },
          { id: "voice", line: "edo.akashi.sato.opt.voice", once: true, when: (g) => who(g) === "lilsis", say: ["edo.akashi.sato.voice.1", "edo.akashi.sato.voice.2"] },
          { id: "bye", line: "edo.akashi.sato.bye.mom", say: ["edo.akashi.sato.bye", "edo.akashi.sato.bye.2"], then: "exit" },
        ],
      },
    },
  };
};

// ======================================================================================================
// taneTree: #36. O-Tane at her door: her daughter will not go in on her first day (the pointer: somebody her own size);
// once O-Kiku is in, Mom asks properly, and the kitchen is hers for an hour (the paddle); and a bed tonight, late or not.
// ======================================================================================================
export const taneTree = (h = {}) => ({
  id: "tane",
  start: (g) => (is(g, "edo.nightDone") ? "after" : is(g, "edo.kikuIn") ? (is(g, "edo.kitchenLent") ? "lent" : "in") : is(g, "edo.taneMet") ? "talk" : "meet"),
  nodes: {
    meet: { say: ["edo.town.tane.meet.1", "edo.town.tane.meet.2"], then: (g) => { g.flag("edo.taneMet", true); return "talk"; } },
    talk: {
      options: [
        { id: "size", clue: true, line: "edo.town.tane.opt.size", when: (g) => who(g) === "mom", say: ["edo.town.tane.size.1"] },
        { id: "cotton", line: "edo.town.tane.opt.cotton", once: true, when: (g) => who(g) === "bigsis", say: ["edo.town.tane.cotton.1", "edo.town.tane.cotton.2", "edo.town.tane.cotton.3"] },
        { id: "kiku", line: "edo.town.tane.opt.kiku", once: true, when: (g) => who(g) === "lilsis", say: ["edo.town.tane.kiku.1", "edo.town.tane.kiku.2"] },
        { id: "byeLil", line: "edo.town.tane.bye.lilsis", when: (g) => who(g) === "lilsis", say: ["edo.town.tane.bye.lilsis.2"], then: "exit" },
        { id: "bye", line: "edo.town.tane.bye.mom", when: (g) => who(g) !== "lilsis", say: ["edo.town.tane.bye"], then: "exit" },
      ],
    },
    in: { say: ["edo.town.tane.in.1"], then: "inTalk" },
    inTalk: {
      options: [
        { id: "kitchen", line: "edo.town.tane.opt.kitchen", when: (g) => who(g) === "mom" && !is(g, "edo.kitchenLent"),
          say: ["edo.town.tane.kitchen.1", "edo.town.tane.kitchen.2", "edo.town.tane.kitchen.3", "edo.town.tane.kitchen.4"],
          then: async (g) => { g.flag("edo.kitchenLent", true); await run(g, h.kitchen); return "paddle"; } },
        { id: "cotton2", line: "edo.town.tane.opt.cotton", once: true, when: (g) => who(g) === "bigsis" && g.asked("tane/cotton") === 0,
          say: ["edo.town.tane.cotton.1", "edo.town.tane.cotton.2", "edo.town.tane.cotton.3"] },
        { id: "bye2", line: "edo.town.tane.bye.mom", say: ["edo.town.tane.bye"], then: "exit" },
      ],
    },
    paddle: { say: ["edo.town.tane.kitchen.5"], then: "lent" },
    lent: {
      options: [
        { id: "sleep", line: "edo.town.tane.opt.sleep", once: true, when: (g) => who(g) === "mom", say: ["edo.town.tane.sleep.1", "edo.town.tane.sleep.2", "edo.town.tane.sleep.3"], set: "edo.taneBed" },
        { id: "bye3", line: "edo.town.tane.bye.mom", say: ["edo.town.tane.bye"], then: "exit" },
      ],
    },
    after: { say: ["edo.town.tane.after"], then: "exit" },
  },
});

// ======================================================================================================
// kikuTree: #36. O-Kiku, seven, says nothing at all. Little Sister has had a first day ("Mine had a HAMSTER."), takes
// her hand, and they go in; the teacher gives the strange girl one character ("mother"); outside again, O-Kiku says her
// one word. Mom and Big Sister get the silence, and their own lines about it.
// ======================================================================================================
export const kikuTree = (h = {}) => ({
  id: "kiku",
  start: (g) => (is(g, "edo.kikuIn") ? "in" : "talk"),
  nodes: {
    talk: {
      options: [
        { id: "first", line: "edo.town.kiku.opt.lilsis", once: true, when: (g) => who(g) === "lilsis", say: ["edo.town.kiku.silent", "edo.town.kiku.lilsis.1"] },
        { id: "hand", line: "edo.town.kiku.opt.hand", when: (g) => who(g) === "lilsis" && g.asked("kiku/first") > 0,
          then: async (g) => { await run(g, h.goIn); return "lesson"; } },
        { id: "mom", line: "edo.town.kiku.opt.mom", once: true, when: (g) => who(g) === "mom", say: ["edo.town.kiku.silent", "edo.town.kiku.mom.1"] },
        { id: "bigsis", line: "edo.town.kiku.opt.bigsis", once: true, when: (g) => who(g) === "bigsis", say: ["edo.town.kiku.silent", "edo.town.kiku.bigsis.1"] },
        { id: "byeLil", line: "edo.town.kiku.bye.lilsis", when: (g) => who(g) === "lilsis", say: ["edo.town.kiku.silent"], then: "exit" },
        { id: "bye", line: "edo.town.kiku.bye.mom", when: (g) => who(g) !== "lilsis", say: ["edo.town.kiku.silent"], then: "exit" },
      ],
    },
    // inside, at the desks; then out to O-Tane
    lesson: { say: ["edo.town.lesson.1", "edo.town.lesson.2", "edo.town.lesson.3", "edo.town.lesson.4"], then: async (g) => { await run(g, h.comeOut); return "mother"; } },
    mother: { say: ["edo.town.lesson.5", "edo.town.lesson.6", "edo.town.lesson.7"], then: (g) => { g.flag("edo.kikuIn", true); return "exit"; } },
    in: { say: ["edo.town.kiku.silent"], then: "exit" },
  },
});

// ======================================================================================================
// shizuTree: #36. O-Shizu, the teacher: busy with a pupil at the door until O-Kiku is in; then she thanks Big Sister for
// the small sister, and draws them the way to Shosha in pictures, no words (edo.knowWay: a clue, kept in short form).
// ======================================================================================================
export const shizuTree = (h = {}) => ({
  id: "shizu",
  start: (g) => (is(g, "edo.nightDone") ? "after" : !is(g, "edo.kikuIn") ? "busy" : is(g, "edo.shizuThanked") ? "talk" : "thanks"),
  nodes: {
    busy: { say: ["edo.town.shizu.busy"], then: "exit" },
    thanks: { say: ["edo.town.shizu.thanks", "edo.town.shizu.thanks.2"], then: (g) => { g.flag("edo.shizuThanked", true); return "talk"; } },
    talk: {
      options: [
        { id: "way", clue: true, line: "edo.town.shizu.opt.way", when: (g) => who(g) === "bigsis",
          say: { 1: ["edo.town.shizu.way.1", "edo.town.shizu.way.2", "edo.town.shizu.way.3", "edo.town.shizu.way.4", "edo.town.shizu.way.5"], more: ["edo.town.shizu.way.again"] },
          set: "edo.knowWay", do: h.drawWay },
        { id: "read", line: "edo.town.shizu.opt.read", once: true, when: (g) => who(g) === "bigsis", say: ["edo.town.shizu.read.1", "edo.town.shizu.read.2"] },
        { id: "mom", line: "edo.town.shizu.opt.mom", once: true, when: (g) => who(g) === "mom", say: ["edo.town.shizu.mom.1", "edo.town.shizu.mom.2"] },
        { id: "lilsis", line: "edo.town.shizu.opt.lilsis", once: true, when: (g) => who(g) === "lilsis", say: ["edo.town.shizu.lilsis.1"] },
        { id: "bye", line: "edo.town.shizu.bye.mom", say: ["edo.town.shizu.bye"], then: "exit" },
      ],
    },
    after: { say: ["edo.town.shizu.after"], then: "exit" },
  },
});

// ======================================================================================================
// tobeiTree: #36. Old Tōbei, the night man, in the daytime: sandals and sweets (one for Little Sister, for the walk); the
// gate at night and the clappers, gate to gate (the plant for "Mind The Fire"); "Hi no yōjin", glossed by him.
// ======================================================================================================
export const tobeiTree = (h = {}) => ({
  id: "tobei",
  start: (g) => (is(g, "edo.nightDone") ? "after" : is(g, "edo.tobeiMet") ? "talk" : "meet"),
  nodes: {
    meet: { say: ["edo.town.tobei.meet"], then: (g) => { g.flag("edo.tobeiMet", true); return "talk"; } },
    talk: {
      options: [
        { id: "sweets", line: "edo.town.tobei.opt.sweets", once: true, when: (g) => who(g) === "lilsis", say: ["edo.town.tobei.sweets.1"],
          then: async (g) => { await run(g, h.sweet); return "sweet"; } },
        { id: "gate", line: "edo.town.tobei.opt.gate", once: true, when: (g) => who(g) === "mom", say: ["edo.town.tobei.gate.1", "edo.town.tobei.gate.2"] },
        { id: "call", line: "edo.town.tobei.opt.call", once: true, when: (g) => who(g) === "bigsis", say: ["edo.town.tobei.call.1", "edo.town.tobei.call.2"] },
        { id: "byeLil", line: "edo.town.tobei.bye.lilsis", when: (g) => who(g) === "lilsis", say: ["edo.town.tobei.bye"], then: "exit" },
        { id: "bye", line: "edo.town.tobei.bye.mom", when: (g) => who(g) !== "lilsis", say: ["edo.town.tobei.bye.2"], then: "exit" },
      ],
    },
    sweet: { say: ["edo.town.tobei.sweets.2"], then: "talk" },
    after: { say: ["edo.town.tobei.after"], then: "exit" },
  },
});

// ======================================================================================================
// umeTree: #37. O-Ume, the keeper: thirteen evenings of the voice; her husband the shipwright, who made the lock for women
// who cannot climb; the riddle (a clue: edo.riddle, edo.oumeMet); her son, once; the rice ball on the step; the slips from
// Osaka and Akashi; the keys; and Big Sister's note against the riddle (the list: edo.listRead).
// ======================================================================================================
export const umeTree = (h = {}) => {
  const riddle = { say: { 1: ["edo.shosha.ume.riddle.1", "edo.shosha.ume.riddle.2"], more: ["edo.shosha.ume.riddle.1"] }, set: ["edo.riddle", "edo.oumeMet"] };
  return {
    id: "ume",
    start: (g) => (is(g, "edo.hallOpen") ? "open" : is(g, "edo.umeGreeted") ? "talk" : "meet"),
    nodes: {
      meet: { say: ["edo.shosha.ume.meet"], then: (g) => { g.flag("edo.umeGreeted", true); return "talk"; } },
      talk: {
        options: [
          { id: "voice", line: "edo.shosha.ume.opt.voice", once: true, when: (g) => who(g) === "mom",
            say: ["edo.shosha.ume.voice.1", "edo.shosha.ume.voice.2", "edo.shosha.ume.voice.3", "edo.shosha.ume.voice.4"] },
          { id: "maker", line: "edo.shosha.ume.opt.maker", once: true, when: (g) => who(g) === "mom",
            say: ["edo.shosha.ume.maker.1", "edo.shosha.ume.maker.2", "edo.shosha.ume.maker.3", "edo.shosha.ume.maker.4", "edo.shosha.ume.maker.5"] },
          { id: "riddle", clue: true, line: "edo.shosha.ume.opt.riddle", when: (g) => who(g) === "mom", ...riddle },
          { id: "riddleBig", clue: true, line: "edo.shosha.ume.opt.riddle.bigsis", when: (g) => who(g) === "bigsis", ...riddle },
          { id: "note", clue: true, line: "edo.shosha.ume.opt.note", when: (g) => who(g) === "bigsis" && is(g, "edo.riddle") && g.has("note"),
            say: { 1: SHOSHA.list, more: [SHOSHA.listAgain] }, set: "edo.listRead" },
          { id: "son", line: "edo.shosha.ume.opt.son", once: true, when: (g) => who(g) === "mom" && g.asked("ume/maker") > 0,
            say: ["edo.shosha.ume.son.1", "edo.shosha.ume.son.2", "edo.shosha.ume.son.3"] },
          { id: "step", line: "edo.shosha.ume.opt.step", once: true, when: (g) => who(g) === "mom", say: ["edo.shosha.ume.step.1", "edo.shosha.ume.step.2"] },
          { id: "natsuslip", line: "edo.shosha.ume.opt.natsuslip", when: (g) => who(g) === "mom" && g.has("natsuslip"),
            say: ["edo.shosha.ume.natsuslip.1"], set: "edo.natsuGiven", do: h.slipNatsu },
          { id: "keys", line: "edo.shosha.ume.opt.keys", once: true, when: (g) => who(g) === "bigsis", say: ["edo.shosha.ume.keys.1"] },
          { id: "hall", line: "edo.shosha.ume.opt.hall", once: true, when: (g) => who(g) === "bigsis", say: ["edo.shosha.ume.hall.1", "edo.shosha.ume.hall.2"] },
          { id: "voiceLil", line: "edo.shosha.ume.opt.voice.lilsis", once: true, when: (g) => who(g) === "lilsis",
            say: ["edo.shosha.ume.voicelil.1", "edo.shosha.ume.voicelil.2", "edo.shosha.ume.voicelil.3", "edo.shosha.ume.voicelil.4"] },
          { id: "fusaslip", line: "edo.shosha.ume.opt.fusaslip", when: (g) => who(g) === "lilsis" && g.has("fusaslip"),
            say: ["edo.shosha.ume.fusaslip.1"], set: "edo.fusaGiven", do: h.slipFusa },
          { id: "byeLil", line: "edo.shosha.ume.bye.lilsis", when: (g) => who(g) === "lilsis", say: ["edo.shosha.ume.bye.lilsis.2"], then: "exit" },
          { id: "bye", line: "edo.shosha.ume.bye.mom", when: (g) => who(g) !== "lilsis", say: ["edo.shosha.ume.bye"], then: "exit" },
        ],
      },
      open: {},                                  // (the hall open: she is inside: hallUmeTree)
    },
  };
};

// ======================================================================================================
// ryokaiTree: #37. Ryōkai, fifteen, a novice, on a step by the stone: he apologizes for the mountain. What is up there,
// which they will not see (the hall over the cliff, the three strongmen and the one who ran away, Benkei's stones, the
// bell, the refectory, the lady-poet's poem, described and not given); women and the mountain; the lamp, the lock, the
// abbot's word; and whether he is frightened of the voice ("My brother's LOUD.").
// ======================================================================================================
export const ryokaiTree = (h = {}) => {
  const up = ["edo.shosha.ryokai.up.1", "edo.shosha.ryokai.up.2", "edo.shosha.ryokai.up.3", "edo.shosha.ryokai.up.4", "edo.shosha.ryokai.up.5", "edo.shosha.ryokai.up.6"];
  return {
    id: "ryokai",
    start: (g) => (is(g, "edo.hallOpen") ? "after" : is(g, "edo.ryokaiMet") ? "talk" : "meet"),
    nodes: {
      meet: { say: ["edo.shosha.ryokai.meet"], then: (g) => { g.flag("edo.ryokaiMet", true); return "talk"; } },
      talk: {
        options: [
          { id: "up", line: "edo.shosha.ryokai.opt.up", once: true, when: (g) => who(g) === "mom" && g.asked("ryokai/upLil") === 0, say: up },
          { id: "upLil", line: "edo.shosha.ryokai.opt.up.lilsis", once: true, when: (g) => who(g) === "lilsis" && g.asked("ryokai/up") === 0, say: up },
          { id: "poem", line: "edo.shosha.ryokai.opt.poem", once: true, when: (g) => who(g) === "mom" && (g.asked("ryokai/up") > 0 || g.asked("ryokai/upLil") > 0),
            say: ["edo.shosha.ryokai.poem.1", "edo.shosha.ryokai.poem.2", "edo.shosha.ryokai.poem.3"] },
          { id: "more", line: "edo.shosha.ryokai.opt.more", once: true, when: (g) => who(g) === "bigsis",
            say: ["edo.shosha.ryokai.more.1", "edo.shosha.ryokai.more.2", "edo.shosha.ryokai.more.3"] },
          { id: "women", line: "edo.shosha.ryokai.opt.women", once: true, when: (g) => who(g) === "bigsis", say: ["edo.shosha.ryokai.women.1", "edo.shosha.ryokai.women.2"] },
          { id: "lock", line: "edo.shosha.ryokai.opt.lock", once: true, when: (g) => who(g) === "bigsis",
            say: ["edo.shosha.ryokai.lock.1", "edo.shosha.ryokai.lock.2", "edo.shosha.ryokai.lock.3", "edo.shosha.ryokai.lock.4", "edo.shosha.ryokai.lock.5"] },
          { id: "scared", line: "edo.shosha.ryokai.opt.scared", once: true, when: (g) => who(g) === "lilsis",
            say: ["edo.shosha.ryokai.scared.1", "edo.shosha.ryokai.scared.2", "edo.shosha.ryokai.scared.3", "edo.shosha.ryokai.scared.4"] },
          { id: "byeLil", line: "edo.shosha.ryokai.bye.lilsis", when: (g) => who(g) === "lilsis", say: ["edo.shosha.ryokai.bye.lilsis.2"], then: "exit" },
          { id: "bye", line: "edo.shosha.ryokai.bye.mom", when: (g) => who(g) !== "lilsis", say: ["edo.shosha.ryokai.bye"], then: "exit" },
        ],
      },
      after: {},                                 // (the hall open: he is at the lattice: hallRyokaiTree)
    },
  };
};

// ======================================================================================================
// tomeTree, wifeTree, girlTree: #37, the women on the bench. Grandmother Tome (thirty tries; the front when it opens),
// the young wife with a baby (sent by her mother-in-law), the girl of eleven with her grandmother's slip ("I'm her feet.").
// ======================================================================================================
const benchTree = (id, met, opts, bye, after) => (h = {}) => ({
  id,
  start: (g) => (is(g, "edo.hallOpen") ? "after" : met && !is(g, met.fact) ? "meet" : "talk"),
  nodes: {
    ...(met ? { meet: { say: [met.line], then: (g) => { g.flag(met.fact, true); return "talk"; } } } : {}),
    talk: {
      options: [
        ...opts.map(([lead, line, say]) => ({ id: lead, line, once: true, when: (g) => who(g) === lead, say })),
        { id: "bye", line: bye[0], say: [bye[1]], then: "exit" },
      ],
    },
    after: { say: [after], then: "exit" },
  },
});
export const tomeTree = benchTree("tome", { fact: "edo.tomeMet", line: "edo.shosha.tome.meet" }, [
  ["mom", "edo.shosha.tome.opt.mom", ["edo.shosha.tome.mom.1"]],
  ["bigsis", "edo.shosha.tome.opt.bigsis", ["edo.shosha.tome.bigsis.1"]],
  ["lilsis", "edo.shosha.tome.opt.lilsis", ["edo.shosha.tome.lilsis.1", "edo.shosha.tome.lilsis.2"]],
], ["edo.shosha.tome.opt.bye", "edo.shosha.tome.bye"], "edo.shosha.tome.after");
export const wifeTree = benchTree("wife", null, [
  ["mom", "edo.shosha.wife.opt.mom", ["edo.shosha.wife.mom.1"]],
  ["bigsis", "edo.shosha.wife.opt.bigsis", ["edo.shosha.wife.bigsis.1"]],
  ["lilsis", "edo.shosha.wife.opt.lilsis", ["edo.shosha.wife.lilsis.1"]],
], ["edo.shosha.wife.opt.bye", "edo.shosha.wife.bye"], "edo.shosha.wife.after");
export const girlTree = benchTree("girl", null, [
  ["mom", "edo.shosha.girl.opt.mom", ["edo.shosha.girl.mom.1"]],
  ["bigsis", "edo.shosha.girl.opt.bigsis", ["edo.shosha.girl.bigsis.1"]],
  ["lilsis", "edo.shosha.girl.opt.lilsis", ["edo.shosha.girl.lilsis.1"]],
], ["edo.shosha.girl.opt.bye", "edo.shosha.girl.bye"], "edo.shosha.girl.after");

// ======================================================================================================
// hallUmeTree, hallRyokaiTree: #38, inside. O-Ume kneeling by the door (before: "When the light's on the wall."; after
// the rice ball: "He ate."); Ryōkai's face at the lattice (before: from out here; after the voice, Mom's question, and
// his exactly true answer).
// ======================================================================================================
export const hallUmeTree = (h = {}) => ({
  id: "hallume",
  start: (g) => (is(g, "edo.sonFed") ? "after" : "wait"),
  nodes: {
    wait: { options: [{ id: "wait", line: "edo.hall.ume.opt.wait", say: ["edo.hall.ume.wait"], then: "exit" }] },
    after: { say: ["edo.hall.ume.after"], then: "exit" },
  },
});
export const hallRyokaiTree = (h = {}) => ({
  id: "hallryokai",
  start: (g) => (is(g, "edo.sonHeard") ? "after" : "before"),
  nodes: {
    before: { say: ["edo.hall.ryokai.before"], then: "exit" },
    after: { options: [{ id: "abbot", line: "edo.hall.ryokai.opt.abbot", say: ["edo.hall.ryokai.abbot.1", "edo.hall.ryokai.abbot.2"], then: "exit" }] },
  },
});

// ======================================================================================================
// sonTree: #38, A Small Door At Sunset. The Son, in Rome, at his own door, as every evening for thirteen of them: a coin-
// sized door in the east wall of the women's hall. Mom has to sit down. "...MOM?" (edo.sonHeard). The menus are the
// family's: Mom first (where, "Have you eaten?", what he has been doing, where he sleeps), Big Sister (the when; Walnut;
// her theory, once the penny is known), Little Sister (her penny; the sacred chickens; brave-scared). The flashlight and
// the rice ball are the scene's (HALL.flash, HALL.riceball). Fed, Mom tells him about tomorrow, and he tells her what
// Dad did wrong: "Hold hands." (edo.holdHands). Then the sun goes: Isaiah 49:15, and the door closes.
// ======================================================================================================
/** Says each line by its speaker: the Son's through the small door (the letterbox's way, with his portrait), the rest
    as ordinary lines. */
export async function sonVoice(g, ids) {
  for (const id of [].concat(ids || [])) {
    const entry = g.lines && g.lines[id];
    if (entry && entry[0] === "son" && typeof g.through === "function") await g.through("son", id);
    else await g.say(id);
  }
}
export const SON = {
  hello: ["edo.hall.son.hello.1", "edo.hall.son.hello.2"],
  known: ["edo.hall.son.temple", "edo.hall.son.mom"],
  told: ["edo.hall.son.told"],
  you: ["edo.hall.son.you.lilsis", "edo.hall.son.you.son", "edo.hall.son.first.lilsis", "edo.hall.son.earlier.son"],
  where: ["edo.hall.son.where.1", "edo.hall.son.where.2", "edo.hall.son.where.3", "edo.hall.son.where.4", "edo.hall.son.where.5", "edo.hall.son.where.6"],
  when: ["edo.hall.son.when.1", "edo.hall.son.where.2", "edo.hall.son.where.3", "edo.hall.son.where.4", "edo.hall.son.where.5", "edo.hall.son.where.6"],
  eaten: ["edo.hall.son.eaten.1", "edo.hall.son.eaten.2"],
  eatenAgain: ["edo.hall.son.eaten.1"],
  days: ["edo.hall.son.days.1", "edo.hall.son.days.2", "edo.hall.son.days.3", "edo.hall.son.days.4", "edo.hall.son.days.5", "edo.hall.son.days.6", "edo.hall.son.days.7"],
  sleep: ["edo.hall.son.sleep.1", "edo.hall.son.sleep.2", "edo.hall.son.sleep.3"],
  walnut: ["edo.hall.son.walnut.1"],
  theory: ["edo.hall.son.theory.1", "edo.hall.son.theory.2"],
  penny: ["edo.hall.son.penny.1"],
  chickens: ["edo.hall.son.chickens.1", "edo.hall.son.chickens.2", "edo.hall.son.chickens.3"],
  scared: ["edo.hall.son.scared.1", "edo.hall.son.scared.2", "edo.hall.son.scared.3"],
  again: ["edo.hall.son.again"],
  againFed: ["edo.hall.son.again.fed"],
  tomorrow: ["edo.hall.son.tomorrow.1", "edo.hall.son.tomorrow.2", "edo.hall.son.tomorrow.3", "edo.hall.son.tomorrow.4"],
  sunset: ["edo.hall.sunset.son"],
  verse: ["edo.hall.sunset.1", "edo.hall.sunset.2", "edo.hall.sunset.3", "edo.hall.sunset.4"],
  after: ["edo.hall.sunset.5", "edo.hall.sunset.6"],
};
export const sonTree = (h = {}) => {
  const said = (list) => async (g) => { await sonVoice(g, list); };
  // the talk, before the rice ball and after it (the eaten question only before; tomorrow only after)
  const chat = [
    { id: "where", line: "edo.hall.son.opt.where", once: true, when: (g) => who(g) === "mom" && g.asked("son/when") === 0, do: said(SON.where) },
    { id: "when", line: "edo.hall.son.opt.when", once: true, when: (g) => who(g) === "bigsis" && g.asked("son/where") === 0, do: said(SON.when) },
    { id: "days", line: "edo.hall.son.opt.days", once: true, when: (g) => who(g) === "mom", do: said(SON.days) },
    { id: "sleep", line: "edo.hall.son.opt.sleep", once: true, when: (g) => who(g) === "mom", do: said(SON.sleep) },
    { id: "walnut", line: "edo.hall.son.opt.walnut", once: true, when: (g) => who(g) === "bigsis", do: said(SON.walnut) },
    { id: "theory", line: "edo.hall.son.opt.theory", once: true, when: (g) => who(g) === "bigsis" && g.asked("son/penny") > 0, do: said(SON.theory) },
    { id: "penny", line: "edo.hall.son.opt.penny", once: true, when: (g) => who(g) === "lilsis", do: said(SON.penny) },
    { id: "chickens", line: "edo.hall.son.opt.chickens", once: true, when: (g) => who(g) === "lilsis", do: said(SON.chickens) },
    { id: "scared", line: "edo.hall.son.opt.scared", once: true, when: (g) => who(g) === "lilsis", do: said(SON.scared) },
  ];
  const bye = { id: "bye", line: "edo.hall.son.opt.bye", then: "exit" };
  return {
    id: "son",
    start: (g) => (is(g, "edo.holdHands") ? "gone" : is(g, "edo.sonFed") ? "fedAgain" : is(g, "edo.sonHeard") ? "again" : "voice"),
    nodes: {
      // his voice; Mom sits down; she answers; he knows her
      voice: { then: async (g) => { await sonVoice(g, SON.hello); await run(g, h.sit); await sonVoice(g, SON.known); g.flag("edo.sonHeard", true); await sonVoice(g, SON.told); return "told"; } },
      // her answer, the player's to give (a menu of one); then he and his little sister, as in Nevada
      told: { options: [{ id: "told", line: "edo.hall.son.told.mom", then: async (g) => { await sonVoice(g, SON.you); return "talk"; } }] },
      talk: {
        options: [
          ...chat,
          // "Have you eaten?": her question from Nevada, and this time an answer is coming (a clue: the rice ball)
          { id: "eaten", clue: true, line: "edo.hall.son.opt.eaten", when: (g) => who(g) === "mom",
            do: async (g) => { await sonVoice(g, g.asked("son/eaten") > 1 ? SON.eatenAgain : SON.eaten); }, set: "edo.eatenAsked" },
          bye,
        ],
      },
      again: { then: async (g) => { await sonVoice(g, SON.again); return "talk"; } },
      // fed: the rest of the talk, and tomorrow (spoken into again: his greeting first)
      fedAgain: { then: async (g) => { await sonVoice(g, SON.againFed); return "fed"; } },
      fed: {
        options: [
          ...chat,
          { id: "tomorrow", line: "edo.hall.son.opt.tomorrow", when: (g) => who(g) === "mom",
            then: async (g) => { await sonVoice(g, SON.tomorrow); g.flag("edo.holdHands", true); return "sunset"; } },
          bye,
        ],
      },
      // the sun goes; the verse; the door closes; O-Ume's question, and Mom's answer
      sunset: { then: async (g) => { await sonVoice(g, SON.sunset); await run(g, h.fade); await sonVoice(g, SON.verse); await run(g, h.close); await sonVoice(g, SON.after); await run(g, h.done); return "exit"; } },
      gone: {},
    },
  };
};

// ======================================================================================================
// HINTS (hint.edo.<beat>.<who><stage>): the stage by the facts, the rule for each below; hintFor gives the line id.
// ======================================================================================================
export const HINTS = {
  ladle: { stages: ["", ".2", ".3", ".4", ".5", ".6", ".7", ".8"],
    rule: "O-Fusa not met (edo.fusaMet): 1; not waded (edo.waded): 2; no crab and Heita's clue not heard (edo.crabClue): 3; no crab (edo.crab): 4; the octopus still has the ladle (edo.ladleFree): 5; the ladle not given back (edo.ladleBack): 6; the riddle not heard (edo.riddle): 7; else 8 (the road west: the card)" },
  supper: { stages: ["", ".2", ".3", ".4", ".5"],
    rule: "O-Kiku not in (edo.kikuIn): 1; the way not known (edo.knowWay): 2; no rice balls (edo.riceballs) and the kitchen not lent (edo.kitchenLent): 3; no rice balls: 4; else 5 (to Shosha)" },
  hall: { stages: ["", ".2", ".3", ".4", ".5", ".6", ".7"],
    rule: "in the close-up with the ear and the post held: 7; with the ear held: 6; else: O-Ume not met (edo.oumeMet): 1; the lock not seen (edo.lockSeen): 2; the list not read against the riddle (edo.listRead): 3; the three things not in their right hands (pin with Little Sister, coin with Mom, comb with Big Sister): 4; else 5" },
  son: { stages: ["", ".2", ".3", ".4"],
    rule: "the voice not heard (edo.sonHeard): 1; the door a coin wide (edo.doorWide): 2; not fed (edo.sonFed): 3; else 4 (the talk to finish: edo.holdHands)" },
};
/** The hint line for a beat ("ladle", "supper", "hall", "son") and a lead, by the facts. */
export function hintFor(g, beat, lead = who(g)) {
  const stage = (n) => `hint.edo.${beat}.${lead}${n > 1 ? "." + n : ""}`;
  if (beat === "ladle") {
    if (!is(g, "edo.fusaMet")) return stage(1);
    if (!is(g, "edo.waded")) return stage(2);
    if (!is(g, "edo.crab")) return stage(is(g, "edo.crabClue") ? 4 : 3);
    if (!is(g, "edo.ladleFree")) return stage(5);
    if (!is(g, "edo.ladleBack")) return stage(6);
    return stage(is(g, "edo.riddle") ? 8 : 7);
  }
  if (beat === "supper") {
    if (!is(g, "edo.kikuIn")) return stage(1);
    if (!is(g, "edo.knowWay")) return stage(2);
    if (!is(g, "edo.riceballs")) return stage(is(g, "edo.kitchenLent") ? 4 : 3);
    return stage(5);
  }
  if (beat === "hall") {
    if (is(g, "edo.earHeld") && is(g, "edo.postHeld")) return stage(7);
    if (is(g, "edo.earHeld")) return stage(6);
    if (!is(g, "edo.oumeMet")) return stage(1);
    if (!is(g, "edo.lockSeen")) return stage(2);
    if (!is(g, "edo.listRead")) return stage(3);
    const right = Object.entries(LOCK.rightHands).every(([item, lead2]) => holds(g, lead2, item));
    return stage(right ? 5 : 4);
  }
  if (beat === "son") {
    if (!is(g, "edo.sonHeard")) return stage(1);
    if (!is(g, "edo.doorWide")) return stage(2);
    if (!is(g, "edo.sonFed")) return stage(3);
    return stage(4);
  }
  return null;
}

/** Every tree, by name, for the tests. */
export const trees = { fusaTree, leaderTree, heitaTree, satoTree, taneTree, kikuTree, shizuTree, tobeiTree, umeTree, ryokaiTree,
  tomeTree, wifeTree, girlTree, hallUmeTree, hallRyokaiTree, sonTree };

// Act Six: By Your Grace. Mom and the girls in Japan, spring 1830 (MERGE-20: new in round twenty; the design is
// briefs/out/edo-design.md, sections 3 and 7; the lines are js/content/lines/edo-a.en.js and edo-b.en.js, the talks
// js/content/talk/edo-a.js and edo-b.js, the scenes js/content/scenes/edo-*.js and the cut-scenes edo-arrive, edo-sail,
// edo-walk and edo-step in js/content/cutscenes/).
// MERGE-21: made bigger in round twenty-one (briefs/out/edo2-design.md, section 7): the road over the Satta Pass, a day on
// the ship, Osaka, the Kyoto boat, the Akashi shore, Himeji town, and the women's hall at the foot of Mount Shosha with the
// Son's small door; new lines in edo-c.en.js (WRITE-21A) and edo-d.en.js (WRITE-21B), talks in talk/edo-c.js and edo-d.js.
// The puzzles are numbered in play order now: round twenty's #24 is #24 and #25, its #25-#27 are #32-#34, its #28-#30
// are #39-#41 (names, beats, facts and line ids kept).
//
// Meanwhile, in another time: Mom, Big Sister and Little Sister come through the coin door expecting the Son, and land
// on a beach under Fuji in the spring of 1830. The act is a journey west in three legs, each its own place on the map:
//
//   the arrival (cut-scene)             Meanwhile, in another time: the beach at Yui, dawn
//   #21 Where, And When (A, Big Sister) a red hood, square-holed coins, a new blue: the metal tiger, 1830
//   #22 Out Of Sight (B, Mom)           the board, the clerk, a baby who will not sleep, three kimonos (the boots stay)
//   #23 Kihei's Table (C, any)          pressed sushi, freely given; grace; "Okage-sama de"; the cat and the mackerel
//   #24 West (Little Sister, then all)  the hens face west; the road; Nishikurasawa; the top of the Satta Pass; a woman's
//                                       pass on the Jizō, given back; Arai; not by road (edo.road)
//   #25 A Captain Who Says Yes (Mom)    Kihei names the ship; Gonroku will not take women; ask O-Masa   (the first leg's gate)
//   Casting Off (cut-scene)             the goodbyes; the ship's boat; the windlass; the sail; "Four days later"
//   #26 Etekō (Big Sister)              the ship's clock runs backwards; the word you don't say at sea
//   #27 Don't Lift The Lid (Little Sister, Mom) Kōta's rice; the Funadama's list; a penny for a coin; she chirps
//   The Uttermost Parts (cut-scene)     the ship by night, Psalm 139; Osaka: the river mouth, the lighter, the Dōjima shore
//   #28 The Dōjima Shore (all)          no ladle; Mom takes the paddle; "My helpers."
//   #29 What The Road God Said (Mom)    the crossroads comb; Jeremiah 31:17; the yomiuri: a boy's voice at Shosha
//   #30 Berlin Blue (Big Sister)        the print shop's marks; the sheet read aloud: the lock no comb opens
//   #31 Three To A Puppet (the girls)   the Inari theatre; in black you're not there; the boy runs home
//   The Kyoto Boat (cut-scene)          the haulers, the food boats, the ferry, north, the rain
//   #32 Under The Cedars (Little Sister) the rain, the praying ground, the window, the mat, a knock on a trapdoor
//   #33 Our Father (Mom, Little Sister)  the room underground; the same prayer; the altar; John 1:5
//   #34 Charcoal, And A Kind Child (all) the constable; nobody lies; the egg; the mirror's cross; the trowel
//   Three days later (card)             everybody else going the other way; Kōriyama, Suma, Maiko; Akashi
//   #35 The Ladle (Little Sister)       the boots are for water; the octopus; the crab; O-Fusa's slip; the riddle
//   The next day (card)                 Himeji
//   #36 Supper For A Voice (each)       O-Kiku's first day; O-Shizu's map; Mom's rice balls
//   #37 What A Ship Gives Its Lady (all three at once) the women's hall: the pin, the coin, the comb; the lock chirps
//   #38 A Small Door At Sunset (Mom)    the Son; more light; a rice ball for Rome; "Hold hands."; Isaiah 49:15
//   Mind The Fire (cut-scene)           the walk back in the dark; the clappers, gate to gate; "The next day"
//   #39 Eight At The Gate (all)         Tomezō's crew is three short; the count; the cross on the tile
//   #40 A Light That Needs No Fire (Little Sister) the warden, his poems, the pink flashlight
//   #41 The Lady Of The Keep (Mom)      the truth; the west window; the mirror's light grows into a door
//   Hold Hands (cut-scene)              the coin, the step, the warden's last poem, "to be continued": the end of the demo
//
// Every beat carries a hint for each of the three: the one who does the job says what to try, the others whose job it
// is. The long puzzles' hints follow how far they have got (WRITE-20A's ids.md and WRITE-20B's ids.md give each stage):
// such a hint is a function of the game listing every line it can give (`lines`), as the Office's are.
//
// The facts a stage reads that are not beats' are the scenes' own, named here so that the scenes set exactly these:
//   #21 edo.clue.red, edo.clue.coins, edo.clue.blue      #22 edo.clerkPassed, edo.babySleeps, edo.clothes
//   #23 edo.kiheiMet, edo.pennyShown                     #24 edo.kiheiWest, edo.hensWest, edo.gonrokuNo, edo.gonrokuWife
//   #25 edo.pipeHeard, edo.unbarred                      #27 edo.sacksHid, edo.pinkOff, edo.momBelow (all three: he is at the door)
//   #28 edo.tomezoDown, edo.trowelBack, edo.crew         #29 edo.shinMet, edo.lightShown
//   #30 edo.truth, edo.window, edo.letterbox (the mirror's light on the hum: a hand's door), edo.doorway (Mom at the west
//       window: a doorway's door)
// (round twenty's numbers above.) MERGE-21, round twenty-one's (WRITE-21A's ids.md and WRITE-21B's give each stage):
//   #24 edo.hensWest, edo.gust, edo.passFound, edo.passBack     #25 edo.kiheiWest (after the road), edo.gonrokuNo, edo.gonrokuWife
//   #26 edo.compassRead, edo.saruSaid, edo.seaWords             #27 edo.kotaMet, edo.lidDown, edo.funadamaList, edo.coinTraded
//   #28 edo.paddle, edo.fedPilgrims                             #29 edo.combAsked, edo.heardShosha, edo.sheetCaught
//   #30 edo.marksSeen, edo.registered                           #31 edo.backstage, edo.hooded, edo.rehearsed, edo.momSeated,
//                                                                   edo.cue1, edo.cue2, edo.cue3
//   #35 to #38: WRITE-21B's hintFor (talk/edo-d.js) reads them: edo.fusaMet, edo.waded, edo.crabClue, edo.crab, edo.ladleFree,
//       edo.riddle; edo.kikuIn, edo.knowWay, edo.kitchenLent, edo.riceballs; edo.oumeMet, edo.lockSeen, edo.listRead,
//       edo.earHeld and edo.postHeld (held, never saved), the three things in their right hands; edo.sonHeard,
//       edo.doorWide, edo.sonFed

import { hintFor as hintD, HINTS as HINTS_D } from "../talk/edo-d.js";      // MERGE-21: WRITE-21B's staged hints for #35-#38

const FAMILY = ["mom", "bigsis", "lilsis"];
const is = (g, fact) => !!g.flag(fact);
/** A hint that follows how far a puzzle has got: fn(g) gives a line; `lines` lists them all. */
const staged = (lines, fn) => Object.assign(fn, { lines });
/** The same staged hint for each of the three: `pick(g)` gives the stage's suffix ("", ".2", ...). */
const stagedAll = (base, suffixes, pick) => Object.fromEntries(FAMILY.map((who) =>
  [who, staged(suffixes.map((s) => `${base}.${who}${s}`), (g) => `${base}.${who}${pick(g)}`)]));
/** MERGE-21: WRITE-21B's hints for a beat of #35-#38 ("ladle", "supper", "hall", "son"), for each of the three. */
const stagedD = (beat) => Object.fromEntries(FAMILY.map((who) =>
  [who, staged(HINTS_D[beat].stages.map((s) => `hint.edo.${beat}.${who}${s}`), (g) => hintD(g, beat, who))]));

export const act = {
  id: 7, title: "Act Six: By Your Grace", era: "edo", gate: "edo.done",
  summary: "Meanwhile, in another time: Mom and the girls come through the coin door expecting the Son, and land on a beach at Yui under Fuji, in their own clothes, in a country where foreigners landing are to be seized. Big Sister cannot read a single sign and works out the year from a fishmonger's red hood, his square-holed coins and the new blue of a print: the metal tiger, 1830. O-Tami hides them from the headman's clerk, Mom sings her baby to sleep, and they are dressed in her old travel clothes (Little Sister keeps her yellow boots); the clerk writes down 'travellers, three, going west', every word of it true. Kihei presses mackerel sushi and will not take anything for it; Little Sister says grace and learns 'arigatō'; Kihei answers 'Okage-sama de', by your grace. The hens all face west; the captain will not take women aboard, and his wife, asked properly, changes his mind. Twelve days by sea, Psalm 139 at the stern rail, Osaka, and north into the hills in the rain: the ground is praying. Under a charcoal-burner's storehouse a hidden family keeps the old faith with no priest for two hundred years; Little Sister prays the Our Father, and Grandmother Sei answers with the same prayer in her old words. In the morning a constable climbs the path; nobody lies, and Little Sister gives him her egg: 'Nothing here but charcoal and a kind child.' The grandmother shows them the cross that her bronze mirror throws in the light, and gives it to Mom; Jinsuke gives them his cousin's trowel. At Himeji they walk in through the castle gate as three of Tomezō's plasterers (eight out, eight back); the young warden Shinnosuke, who must keep the top of the keep tonight, is given a light with no fire in it; at the top Mom tells him the truth, he opens the west window, and the mirror's light on the humming wall grows, as she backs into the sunset, into a door with a cross in it. Hold hands. To be continued.",
  beats: [
    { id: "edo.arrive", kind: "cutscene", title: "Meanwhile, in another time", lead: "family", scene: "edo-village", needs: ["office.done"], sets: "edo.arrived" },

    { id: "edo.when", kind: "puzzle", chain: "A", title: "Where, And When: a red hood, square-holed coins and a new blue (the metal tiger, 1830)", lead: "bigsis", scene: "edo-fishshop",
      needs: ["edo.arrived"], sets: "edo.when",
      hint: {
        mom: "hint.edo.when.mom",
        bigsis: staged(["hint.edo.when.bigsis", "hint.edo.when.bigsis.2", "hint.edo.when.bigsis.3", "hint.edo.when.bigsis.4", "hint.edo.when.bigsis.5"], (g) => {
          const red = is(g, "edo.clue.red"), coins = is(g, "edo.clue.coins"), blue = is(g, "edo.clue.blue");
          if (!red && !coins && !blue) return "hint.edo.when.bigsis";
          if (!red) return "hint.edo.when.bigsis.2";
          if (!coins) return "hint.edo.when.bigsis.3";
          if (!blue) return "hint.edo.when.bigsis.4";
          return "hint.edo.when.bigsis.5";
        }),
        lilsis: "hint.edo.when.lilsis",
      } },
    { id: "edo.dressed", kind: "puzzle", chain: "B", title: "Out Of Sight: the board, the clerk, a baby and three kimonos", lead: "mom", scene: "edo-village",
      needs: ["edo.arrived"], sets: "edo.dressed",
      hint: {
        mom: staged(["hint.edo.dressed.mom", "hint.edo.dressed.mom.2", "hint.edo.dressed.mom.3", "hint.edo.dressed.mom.4"], (g) => {
          if (!is(g, "edo.clerkPassed")) return "hint.edo.dressed.mom";
          if (!is(g, "edo.babySleeps")) return "hint.edo.dressed.mom.2";
          if (!is(g, "edo.clothes")) return "hint.edo.dressed.mom.3";
          return "hint.edo.dressed.mom.4";
        }),
        bigsis: "hint.edo.dressed.bigsis",
        lilsis: "hint.edo.dressed.lilsis",
      } },
    { id: "edo.fed", kind: "puzzle", chain: "C", title: "Kihei's Table: pressed sushi, freely given", lead: "family", scene: "edo-fishshop",
      needs: ["edo.arrived"], sets: "edo.fed",
      hint: {
        mom: staged(["hint.edo.fed.mom", "hint.edo.fed.mom.2"], (g) => (is(g, "edo.kiheiMet") ? "hint.edo.fed.mom.2" : "hint.edo.fed.mom")),
        bigsis: staged(["hint.edo.fed.bigsis", "hint.edo.fed.bigsis.2"], (g) => (is(g, "edo.kiheiMet") ? "hint.edo.fed.bigsis.2" : "hint.edo.fed.bigsis")),
        lilsis: staged(["hint.edo.fed.lilsis", "hint.edo.fed.lilsis.2"], (g) => (is(g, "edo.pennyShown") ? "hint.edo.fed.lilsis.2" : "hint.edo.fed.lilsis")),
      } },
    // MERGE-21: #24 West: the hens, the road, Nishikurasawa, the top of the Satta Pass, a woman's pass, Arai: not by road
    { id: "edo.road", kind: "puzzle", chain: "B", title: "West: the hens, the road over the Satta Pass, a woman's pass given back, and Arai (not by road)", lead: ["lilsis", "family"], scene: "edo-satta",
      needs: ["edo.dressed"], sets: "edo.noRoad",
      hint: stagedAll("hint.edo.road", ["", ".2", ".3", ".4", ".5"],
        (g) => (!is(g, "edo.hensWest") ? "" : !is(g, "edo.gust") ? ".2" : !is(g, "edo.passFound") ? ".3" : !is(g, "edo.passBack") ? ".4" : ".5")) },
    // #25 A Captain Who Says Yes (round twenty's #24, second half): Kihei names the ship only after the road
    { id: "edo.west", kind: "puzzle", chain: "A", title: "A Captain Who Says Yes: Kihei names the ship, Gonroku says no, and O-Masa asked properly (the first leg's gate)", lead: "mom", scene: "edo-village",
      needs: ["edo.noRoad", "edo.fed"], sets: "edo.west",
      hint: {      // MERGE-21: WRITE-21A's stages first (hint.edo.west.ship.*), then round twenty's
        mom: staged(["hint.edo.west.ship.mom", "hint.edo.west.ship.mom.2", "hint.edo.west.mom.2"],
          (g) => (!is(g, "edo.kiheiWest") ? "hint.edo.west.ship.mom" : !is(g, "edo.gonrokuNo") ? "hint.edo.west.ship.mom.2" : "hint.edo.west.mom.2")),
        bigsis: staged(["hint.edo.west.ship.bigsis", "hint.edo.west.ship.bigsis.2", "hint.edo.west.bigsis", "hint.edo.west.bigsis.2"],
          (g) => (!is(g, "edo.kiheiWest") ? "hint.edo.west.ship.bigsis" : !is(g, "edo.gonrokuNo") ? "hint.edo.west.ship.bigsis.2"
            : is(g, "edo.gonrokuWife") ? "hint.edo.west.bigsis.2" : "hint.edo.west.bigsis")),
        lilsis: staged(["hint.edo.west.ship.lilsis", "hint.edo.west.ship.lilsis.2", "hint.edo.west.lilsis.3"],
          (g) => (!is(g, "edo.kiheiWest") ? "hint.edo.west.ship.lilsis" : !is(g, "edo.gonrokuNo") ? "hint.edo.west.ship.lilsis.2" : "hint.edo.west.lilsis.3")),
      } },
    // MERGE-21: the ship is theirs at first light: the goodbyes, then Casting Off (the ship's boat, the windlass, the sail);
    // Big Sister will not sail out of a year she cannot name (#21 first).
    { id: "edo.castoff", kind: "cutscene", title: "Casting Off", lead: "family", scene: "edo-village", needs: ["edo.west", "edo.when"], sets: "edo.aboard",
      hint: { mom: "hint.edo.castoff.mom", bigsis: "hint.edo.castoff.bigsis", lilsis: "hint.edo.castoff.lilsis" } },
    // #26 and #27, the deck by day, in either order. PUZZLE-25 (docs/PUZZLES-japan.md): each stage's hint is the next step,
    // a rung at a time: #26 the goal; the glare (the box seen); the needle (the card shaded); the call (the clock read); the
    // sailors' word (after "Monkey!"); the call again (the word known). #27 the goal (Denzō's, until something is done); the
    // lid; the coin; the list.
    { id: "edo.heading", kind: "puzzle", chain: "A", title: "Etekō: the ship's clock runs backwards, and the word you don't say at sea", lead: "bigsis", scene: "edo-deck",
      needs: ["edo.aboard"], sets: "edo.headingCalled",
      hint: stagedAll("hint.edo.heading", ["", ".2", ".3", ".4", ".5", ".6"],
        (g) => (!is(g, "edo.compassRead") ? (is(g, "edo.cardShaded") ? ".3" : is(g, "edo.boxSeen") ? ".2" : "")
          : is(g, "edo.seaWords") ? ".6" : is(g, "edo.saruSaid") ? ".5" : ".4")) },
    { id: "edo.chirp", kind: "puzzle", chain: "B", title: "Don't Lift The Lid: Kōta's rice, the Funadama's list, a penny for a coin, and she chirps", lead: ["lilsis", "mom"], scene: "edo-deck",
      needs: ["edo.aboard"], sets: "edo.chirped",
      hint: stagedAll("hint.edo.chirp", ["", ".2", ".3", ".4"],
        (g) => (!is(g, "edo.denzoMet") && !is(g, "edo.lidDown") && !is(g, "edo.coinTraded") && !is(g, "edo.funadamaList") ? ""
          : !is(g, "edo.lidDown") ? ".2" : !is(g, "edo.coinTraded") ? ".3" : ".4")) },
    // The night at sea, Psalm 139, "Eight days later", Osaka: the river mouth, the lighter, the Dōjima shore
    { id: "edo.sail", kind: "cutscene", title: "The Uttermost Parts (the night at sea; Osaka)", lead: "family", scene: "edo-deck", needs: ["edo.headingCalled", "edo.chirped"], sets: "edo.sailed" },

    // MERGE-21: Osaka (#28-#31), then the Kyoto boat
    { id: "edo.alms", kind: "puzzle", title: "The Dōjima Shore: no ladle, the paddle, the pilgrims fed, and \"My helpers.\"", lead: "family", scene: "edo-dojima",
      needs: ["edo.sailed"], sets: "edo.vouched",
      hint: stagedAll("hint.edo.alms", ["", ".2", ".3"], (g) => (!is(g, "edo.paddle") ? "" : !is(g, "edo.fedPilgrims") ? ".2" : ".3")) },
    { id: "edo.heard", kind: "puzzle", chain: "A", title: "What The Road God Said: the crossroads comb, the yomiuri's chant, and a boy's voice at Shosha", lead: "mom", scene: "edo-street",
      needs: ["edo.vouched"], sets: "edo.combGiven",
      hint: stagedAll("hint.edo.heard", ["", ".2", ".3", ".4"],
        (g) => (!is(g, "edo.combAsked") ? "" : !is(g, "edo.heardShosha") ? ".2" : !is(g, "edo.sheetCaught") ? ".3" : ".4")) },
    { id: "edo.read", kind: "puzzle", chain: "B", title: "Berlin Blue: the print shop's marks, and the sheet read aloud", lead: "bigsis", scene: "edo-street",
      needs: ["edo.vouched"], sets: "edo.sheetRead",      // (beside #29: the reading needs the sheet #29 catches; the printing does not)
      hint: stagedAll("hint.edo.read", ["", ".2", ".3"], (g) => (!is(g, "edo.marksSeen") ? "" : !is(g, "edo.registered") ? ".2" : ".3")) },
    { id: "edo.troupe", kind: "puzzle", chain: "C", title: "Three To A Puppet: in black you're not there, and the boy runs home", lead: ["bigsis", "lilsis"], scene: "edo-theatre",
      needs: ["edo.combGiven"], sets: "edo.troupeTaken",      // (after #29: Tatsu follows them from the crossroads)
      hint: stagedAll("hint.edo.troupe", ["", ".2", ".3", ".4", ".5", ".6", ".7", ".8"],
        (g) => (!is(g, "edo.backstage") ? "" : !is(g, "edo.hooded") ? ".2" : !is(g, "edo.rehearsed") ? ".3" : !is(g, "edo.momSeated") ? ".4"
          : !is(g, "edo.cue1") ? ".5" : !is(g, "edo.cue2") ? ".6" : !is(g, "edo.cue3") ? ".7" : ".8")) },
    { id: "edo.boat", kind: "cutscene", title: "The Kyoto Boat (up the river, round Osaka, north into the rain)", lead: "family", scene: "edo-theatre", needs: ["edo.troupeTaken", "edo.sheetRead"], sets: "edo.boated",
      hint: { mom: "hint.edo.boat.mom", bigsis: "hint.edo.boat.bigsis", lilsis: "hint.edo.boat.lilsis" } },

    { id: "edo.hidden", kind: "puzzle", title: "Under The Cedars: the praying ground, the window, the mat, a knock on a trapdoor", lead: "lilsis", scene: "edo-cedars",
      needs: ["edo.boated"], sets: "edo.hidden",      // MERGE-21: by the Kyoto boat now (was edo.sailed)
      hint: stagedAll("hint.edo.hidden", ["", ".2", ".3"], (g) => (!is(g, "edo.pipeHeard") ? "" : !is(g, "edo.unbarred") ? ".2" : ".3")) },
    { id: "edo.trusted", kind: "puzzle", title: "Our Father: the room underground, and the same prayer", lead: ["mom", "lilsis"], scene: "edo-chapel",
      needs: ["edo.hidden"], sets: "edo.trusted",
      hint: { mom: "hint.edo.trusted.mom", bigsis: "hint.edo.trusted.bigsis", lilsis: "hint.edo.trusted.lilsis" } },
    { id: "edo.mirror", kind: "puzzle", title: "Charcoal, And A Kind Child: the constable, the egg, and the mirror's cross", lead: "family", scene: "edo-storehouse",
      needs: ["edo.trusted"], sets: "edo.mirror",
      // SCENES-20B (to test; MERGE-20 makes it): ".0" the night, before O-Rin's warning; ".5" the constable gone, the mirror to come
      hint: stagedAll("hint.edo.mirror", [".0", "", ".2", ".3", ".4", ".5"],
        (g) => (!is(g, "edo.watch") ? ".0" : is(g, "edo.constableGone") ? ".5" : !is(g, "edo.sacksHid") ? "" : !is(g, "edo.pinkOff") ? ".2" : !is(g, "edo.momBelow") ? ".3" : ".4")) },
    { id: "edo.walk", kind: "cutscene", title: "Three days later (Akashi)", lead: "family", scene: "edo-akashi", needs: ["edo.mirror"], sets: "edo.walked",      // MERGE-21: to Akashi now (was Himeji)
      // SCENES-20B (to test; MERGE-20 makes it): after the mirror, up the ladder and on (the room's last moment is played)
      hint: { mom: "hint.edo.mirror.mom.6", bigsis: "hint.edo.mirror.bigsis.6", lilsis: "hint.edo.mirror.lilsis.6" } },

    // MERGE-21: the Akashi shore (#35), the card to Himeji, Himeji town (#36), the women's hall (#37, #38), the night
    { id: "edo.ladle", kind: "puzzle", title: "The Ladle: boots are for water, the octopus, the crab, and O-Fusa's slip", lead: "lilsis", scene: "edo-akashi",
      needs: ["edo.walked"], sets: "edo.ladleBack", hint: stagedD("ladle") },
    { id: "edo.walk2", kind: "cutscene", title: "The next day (Himeji)", lead: "family", scene: "edo-akashi", needs: ["edo.ladleBack"], sets: "edo.inHimeji",
      hint: stagedD("ladle") },      // (WRITE-21B's ladle stages 7 and 8: the riddle, if not heard; then west)
    { id: "edo.supper", kind: "puzzle", title: "Supper For A Voice: O-Kiku's first day, O-Shizu's map, and Mom's rice balls", lead: "family", scene: "edo-town",
      needs: ["edo.inHimeji"], sets: "edo.supperMade", hint: stagedD("supper") },
    { id: "edo.hall", kind: "puzzle", title: "What A Ship Gives Its Lady: the women's hall, the pin, the coin and the comb, three hands at once", lead: "family", scene: "edo-shosha",
      needs: ["edo.supperMade"], sets: "edo.hallOpen", hint: stagedD("hall") },
    { id: "edo.son", kind: "puzzle", title: "A Small Door At Sunset: the Son, more light, a rice ball for Rome, and \"Hold hands.\"", lead: "mom", scene: "edo-hall",
      needs: ["edo.hallOpen"], sets: "edo.holdHands", hint: stagedD("son") },
    { id: "edo.night", kind: "cutscene", title: "Mind The Fire (the walk back; the next day)", lead: "family", scene: "edo-hall", needs: ["edo.holdHands"], sets: "edo.nightDone" },

    { id: "edo.inside", kind: "puzzle", title: "Eight At The Gate: Tomezō's three missing hands, and the cross on the tile", lead: "family", scene: "edo-castle",
      needs: ["edo.nightDone"], sets: "edo.inside",      // MERGE-21: after the night at Himeji (was edo.walked)
      hint: stagedAll("hint.edo.inside", ["", ".2", ".3", ".4"],
        (g) => (!is(g, "edo.tomezoDown") ? "" : !is(g, "edo.trowelBack") ? ".2" : !is(g, "edo.crew") ? ".3" : ".4")) },
    { id: "edo.up", kind: "puzzle", title: "A Light That Needs No Fire: the warden, his poems, the pink flashlight", lead: "lilsis", scene: "edo-keep",
      needs: ["edo.inside"], sets: "edo.up",
      hint: stagedAll("hint.edo.up", ["", ".2", ".3"], (g) => (!is(g, "edo.shinMet") ? "" : !is(g, "edo.lightShown") ? ".2" : ".3")) },
    { id: "edo.door", kind: "puzzle", title: "The Lady Of The Keep: the truth, the west window, the mirror's light", lead: "mom", scene: "edo-keeptop",
      needs: ["edo.up"], sets: "edo.door",
      hint: stagedAll("hint.edo.door", ["", ".2", ".3", ".4", ".5"], (g) => {
        if (!is(g, "edo.truth")) return "";
        if (!is(g, "edo.window")) return ".2";
        if (!is(g, "edo.letterbox")) return ".3";
        return is(g, "edo.doorway") ? ".5" : ".4";
      }) },
    { id: "edo.end", kind: "gate", title: "Hold Hands (the end of the demo)", lead: "family", scene: "edo-keeptop", needs: ["edo.door"], sets: "edo.done" },
  ],
};

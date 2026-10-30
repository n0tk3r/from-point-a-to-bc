// Act Six: By Your Grace. Mom and the girls in Japan, spring 1830 (MERGE-20: new in round twenty; the design is
// briefs/out/edo-design.md, sections 3 and 7; the lines are js/content/lines/edo-a.en.js and edo-b.en.js, the talks
// js/content/talk/edo-a.js and edo-b.js, the scenes js/content/scenes/edo-*.js and the cut-scenes edo-arrive, edo-sail,
// edo-walk and edo-step in js/content/cutscenes/).
//
// Meanwhile, in another time: Mom, Big Sister and Little Sister come through the coin door expecting the Son, and land
// on a beach under Fuji in the spring of 1830. The act is a journey west in three legs, each its own place on the map:
//
//   the arrival (cut-scene)             Meanwhile, in another time: the beach at Yui, dawn
//   #21 Where, And When (A, Big Sister) a red hood, square-holed coins, a new blue: the metal tiger, 1830
//   #22 Out Of Sight (B, Mom)           the board, the clerk, a baby who will not sleep, three kimonos (the boots stay)
//   #23 Kihei's Table (C, any)          pressed sushi, freely given; grace; "Okage-sama de"; the cat and the mackerel
//   #24 West (Little Sister, then Mom)  the hens face west; Gonroku will not take women; ask O-Masa   (the first leg's gate)
//   The Uttermost Parts (cut-scene)     the ship by night, Psalm 139, twelve days, Osaka
//   #25 Under The Cedars (Little Sister) the rain, the praying ground, the window, the mat, a knock on a trapdoor
//   #26 Our Father (Mom, Little Sister)  the room underground; the same prayer; the altar; John 1:5
//   #27 Charcoal, And A Kind Child (all) the constable; nobody lies; the egg; the mirror's cross; the trowel
//   Three days later (card)             everybody else going the other way
//   #28 Eight At The Gate (all)         Tomezō's crew is three short; the count; the cross on the tile
//   #29 A Light That Needs No Fire (Little Sister) the warden, his poems, the pink flashlight
//   #30 The Lady Of The Keep (Mom)      the truth; the west window; the mirror's light grows into a door
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

const FAMILY = ["mom", "bigsis", "lilsis"];
const is = (g, fact) => !!g.flag(fact);
/** A hint that follows how far a puzzle has got: fn(g) gives a line; `lines` lists them all. */
const staged = (lines, fn) => Object.assign(fn, { lines });
/** The same staged hint for each of the three: `pick(g)` gives the stage's suffix ("", ".2", ...). */
const stagedAll = (base, suffixes, pick) => Object.fromEntries(FAMILY.map((who) =>
  [who, staged(suffixes.map((s) => `${base}.${who}${s}`), (g) => `${base}.${who}${pick(g)}`)]));

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
    { id: "edo.west", kind: "puzzle", chain: "A", title: "West: the hens, Gonroku's ship, and O-Masa asked properly (the first leg's gate)", lead: ["lilsis", "mom"], scene: "edo-village",
      needs: ["edo.dressed", "edo.fed"], sets: "edo.west",
      hint: {
        mom: staged(["hint.edo.west.mom", "hint.edo.west.mom.2"], (g) => (is(g, "edo.gonrokuNo") ? "hint.edo.west.mom.2" : "hint.edo.west.mom")),
        bigsis: staged(["hint.edo.west.bigsis", "hint.edo.west.bigsis.2"], (g) => (is(g, "edo.gonrokuWife") ? "hint.edo.west.bigsis.2" : "hint.edo.west.bigsis")),
        lilsis: staged(["hint.edo.west.lilsis", "hint.edo.west.lilsis.2", "hint.edo.west.lilsis.3"], (g) => {
          if (!is(g, "edo.hensWest")) return "hint.edo.west.lilsis";
          return is(g, "edo.gonrokuNo") ? "hint.edo.west.lilsis.3" : "hint.edo.west.lilsis.2";
        }),
      } },
    // The ship is theirs at first light: the goodbyes (the village's), then the voyage. Mom's third hint is for this moment.
    { id: "edo.sail", kind: "cutscene", title: "The Uttermost Parts (the voyage; Osaka)", lead: "family", scene: "edo-village", needs: ["edo.west", "edo.when"], sets: "edo.sailed",      // (SCENES-20A: the ship waits for #21: edo.sail.notyet.bigsis)
      hint: { mom: "hint.edo.west.mom.3", bigsis: "hint.edo.west.mom.3", lilsis: "hint.edo.west.mom.3" } },

    { id: "edo.hidden", kind: "puzzle", title: "Under The Cedars: the praying ground, the window, the mat, a knock on a trapdoor", lead: "lilsis", scene: "edo-cedars",
      needs: ["edo.sailed"], sets: "edo.hidden",
      hint: stagedAll("hint.edo.hidden", ["", ".2", ".3"], (g) => (!is(g, "edo.pipeHeard") ? "" : !is(g, "edo.unbarred") ? ".2" : ".3")) },
    { id: "edo.trusted", kind: "puzzle", title: "Our Father: the room underground, and the same prayer", lead: ["mom", "lilsis"], scene: "edo-chapel",
      needs: ["edo.hidden"], sets: "edo.trusted",
      hint: { mom: "hint.edo.trusted.mom", bigsis: "hint.edo.trusted.bigsis", lilsis: "hint.edo.trusted.lilsis" } },
    { id: "edo.mirror", kind: "puzzle", title: "Charcoal, And A Kind Child: the constable, the egg, and the mirror's cross", lead: "family", scene: "edo-storehouse",
      needs: ["edo.trusted"], sets: "edo.mirror",
      // SCENES-20B (to test; MERGE-20 makes it): ".0" the night, before O-Rin's warning; ".5" the constable gone, the mirror to come
      hint: stagedAll("hint.edo.mirror", [".0", "", ".2", ".3", ".4", ".5"],
        (g) => (!is(g, "edo.watch") ? ".0" : is(g, "edo.constableGone") ? ".5" : !is(g, "edo.sacksHid") ? "" : !is(g, "edo.pinkOff") ? ".2" : !is(g, "edo.momBelow") ? ".3" : ".4")) },
    { id: "edo.walk", kind: "cutscene", title: "Three days later (Himeji)", lead: "family", scene: "edo-castle", needs: ["edo.mirror"], sets: "edo.walked",
      // SCENES-20B (to test; MERGE-20 makes it): after the mirror, up the ladder and on (the room's last moment is played)
      hint: { mom: "hint.edo.mirror.mom.6", bigsis: "hint.edo.mirror.bigsis.6", lilsis: "hint.edo.mirror.lilsis.6" } },

    { id: "edo.inside", kind: "puzzle", title: "Eight At The Gate: Tomezō's three missing hands, and the cross on the tile", lead: "family", scene: "edo-castle",
      needs: ["edo.walked"], sets: "edo.inside",
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

// Act Four: the middle of Nevada, the next morning. A beat with three leads carries one hint from each of them.
// docs/PUZZLES-the-present.md is the act written out.
//
// NEVADA-12SA (round twelve, SCENES-12): the act as expanded (briefs/out/nevada-expansion-design.md). The old-timer is
// Grandpa Joe, the coin is his raccoon's (Big Sister trades for it), the store has an inside (js/content/scenes/nevada-store.js)
// and Grandma Jolene's hens, the flash of the coin (#9) is no longer the gate but the middle of the act, the Son is heard
// through the little door it opens (the letterbox), the sun shade from the store's window held in the low sun opens a
// door as wide as a windshield (#12), and the family walks through it (#13, the gate: nevada.left). The cut-scene
// "Backup" (js/content/cutscenes/backup.js) and Act Five follow (js/content/acts/limo.js); `demo.done` is set at Act
// Five's end now.
//
// Nothing of the family's faith is a beat, and no puzzle knows of it (briefs/WEAVE.md). It hangs on moments that were
// already here: the coin, when it is read, is the coin of the tribute money (Matthew 22:21); before the coin goes up
// they pray; and after "Daddy's EARLY" Mom has Psalm 31:15, before the last two lines. At the walk through, Grandpa Joe
// says the first half of Psalm 121:8 and Mom the second. Nor is anything they bring from the house needed here: Little
// Sister's flashlight gets an answer of its own where the tracks stop, and that is all.
// The author's two rules of 7 October (briefs/DATING.md) are not beats either: the notice seals sectors 44 and 1921 (the
// Bible's own count of the years), and the chickens run through it (Jolene's hens; what Little Sister hears first).

const family = (id) => ({ mom: `hint.${id}.mom`, bigsis: `hint.${id}.bigsis`, lilsis: `hint.${id}.lilsis` });

export const act = {
  id: 4, title: "Act Four: The Last Stop Before Nothing", era: "nevada", gate: "nevada.left",
  summary: "The middle of Nevada, the next morning, at Grandpa Joe's Last Stop. Grandpa Joe saw the low sun flash off the wagon and the sky open where the flash fell, and the government has fenced off the desert for 'elevated radiation'. Mom asks him nicely and he tells it; the silver coin that fell out of a clear sky is his raccoon's, and Ranger trades: Big Sister holds out the mirror shades Mom bought in the store, flat on both hands, and gets the coin, warm, and reads it. Little Sister keeps the man in gray busy while her sister reads the notice: the closed sectors are not places but years. In the store, Grandma Jolene's hens have stood facing the fence since the day the sky opened; Little Sister stands in the row with them and sees that they are guarding, and they lay again. They pray, and flash the morning sun off the coin where the tracks stop: a door the size of the coin, with chickens on the other side of it. Little Sister has been right since the night before: Daddy is not lost, Daddy is early. Through the little door they hear the Son, in Rome, in 44 B.C., who warns them not to come; Little Sister sends him a penny for luck. A bigger shine makes a bigger door: Grandpa Joe holds the sun shade from Jolene's window in the low sun, and the door opens as wide as a windshield. After the goodbyes, and the psalm said in two halves on a stranger's porch, they go through it hand in hand.",
  beats: [
    { id: "nevada.arrive", kind: "cutscene", title: "Where the map stops", lead: "family", scene: "nevada-roadside", needs: ["home.left"], sets: "nevada.arrived" },
    { id: "nevada.witness", kind: "puzzle", chain: "A", title: "Ask Grandpa Joe nicely, and prove you are family", lead: "mom", scene: "nevada-roadside", needs: ["nevada.arrived"], sets: "nevada.witness", hint: family("nevada.witness") },
    { id: "nevada.ranger", kind: "puzzle", chain: "A", title: "Trade Ranger the mirror shades for the coin, both hands out", lead: "bigsis", scene: "nevada-roadside", needs: ["nevada.witness"], sets: "nevada.traded", hint: family("nevada.ranger") },
    { id: "nevada.coin", kind: "puzzle", chain: "A", title: "Let Big Sister read the coin that fell out of the sky", lead: "bigsis", scene: "nevada-roadside", needs: ["nevada.traded"], sets: "nevada.coinRead", hint: family("nevada.coin") },
    { id: "nevada.distract", kind: "puzzle", chain: "B", title: "Ask the man in gray two hundred questions", lead: "lilsis", scene: "nevada-roadside", needs: ["nevada.arrived"], sets: "nevada.distracted", hint: family("nevada.distract") },
    { id: "nevada.notice", kind: "puzzle", chain: "B", title: "Read the notice on the fence", lead: "bigsis", scene: "nevada-roadside", needs: ["nevada.distracted"], sets: "nevada.notice", hint: family("nevada.notice") },
    { id: "nevada.hens", kind: "puzzle", chain: "C", title: "Stand in the row with Grandma Jolene's hens", lead: "lilsis", scene: "nevada-store", needs: ["nevada.arrived"], sets: "nevada.jolene", hint: family("nevada.hens") },
    { id: "nevada.tracks", kind: "puzzle", title: "Flash the morning sun off the coin onto the place where the tracks stop (and a prayer first)", lead: "family", scene: "nevada-roadside", needs: ["nevada.coinRead", "nevada.notice"], sets: "nevada.doorOpen", hint: family("nevada.tracks") },
    { id: "nevada.letterbox", kind: "puzzle", title: "Say hello into the little door: the Son is on the other side", lead: "family", scene: "nevada-roadside", needs: ["nevada.doorOpen"], sets: "nevada.heardSon", hint: family("nevada.letterbox") },
    // (Little Sister's hint for this one, "Grandma Jolene said I could have anything. I did the chickens.", is true only once the hens are done: hence nevada.jolene.)
    { id: "nevada.shade", kind: "puzzle", title: "Have Grandpa Joe hold the sun shade from the window in the low sun", lead: "family", scene: "nevada-roadside", needs: ["nevada.doorOpen", "nevada.jolene", "nevada.heardSon"], sets: "nevada.wideOpen", hint: family("nevada.shade") },
    { id: "nevada.through", kind: "gate", title: "Say goodbye, and go through the door hand in hand", lead: "family", scene: "nevada-roadside", needs: ["nevada.wideOpen"], sets: "nevada.left", hint: family("nevada.through") },
  ],
};

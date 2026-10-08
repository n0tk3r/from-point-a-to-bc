// Act Four: the middle of Nevada, the next morning. A beat with three leads carries one hint from each of them.
// docs/PUZZLES-the-present.md is the act written out.
//
// Nothing of the family's faith is a beat, and no puzzle knows of it (briefs/WEAVE.md). It hangs on moments that were
// already here: the coin, when it is read, is the coin of the tribute money (Matthew 22:21); before the coin goes up
// they pray; and after "Daddy's EARLY" Mom has Psalm 31:15, before the last two lines. Nor is anything they bring
// from the house needed here: Little Sister's flashlight gets an answer of its own where the tracks stop, and that is all.
// The author's two rules of 7 October (briefs/DATING.md) are not beats either: the notice seals sectors 44 and 1921 (the
// Bible's own count of the years), and the chickens run through it (the old-timer's hens; what Little Sister hears first).

const family = (id) => ({ mom: `hint.${id}.mom`, bigsis: `hint.${id}.bigsis`, lilsis: `hint.${id}.lilsis` });

export const act = {
  id: 4, title: "Act Four: The Last Stop Before Nothing", era: "nevada", gate: "demo.done",
  summary: "The middle of Nevada, the next morning. A witness saw the low sun flash off the wagon and the sky open where the flash fell, and the government has fenced off the desert for 'elevated radiation'. Mom gets the witness talking, Little Sister keeps the man in gray busy, and Big Sister reads a coin and a notice and sees that the closed sectors are not places but years. Where the tire tracks stop there is nothing to see, and a hum; and the old-timer's hens have stood facing the fence since the day the sky opened. They pray first, and then flash the morning sun off the coin onto the place, and a door opens exactly the size of the coin, with chickens on the other side of it. Big Sister names the two years: the Ides of March, and the year Abram went down into Egypt. Little Sister has been right since the night before: Daddy is not lost, Daddy is early. And Mom has the psalm for it: 'My times are in thy hand' (Psalm 31:15).",
  beats: [
    { id: "nevada.arrive", kind: "cutscene", title: "Where the map stops", lead: "family", scene: "nevada-roadside", needs: ["home.left"], sets: "nevada.arrived" },
    { id: "nevada.witness", kind: "puzzle", chain: "A", title: "Ask the old-timer nicely, and prove you are family", lead: "mom", scene: "nevada-roadside", needs: ["nevada.arrived"], sets: "nevada.witness", hint: family("nevada.witness") },
    { id: "nevada.coin", kind: "puzzle", chain: "A", title: "Hand Big Sister the coin that fell out of the sky", lead: "bigsis", scene: "nevada-roadside", needs: ["nevada.witness"], sets: "nevada.coinRead", hint: family("nevada.coin") },
    { id: "nevada.distract", kind: "puzzle", chain: "B", title: "Ask the man in gray two hundred questions", lead: "lilsis", scene: "nevada-roadside", needs: ["nevada.arrived"], sets: "nevada.distracted", hint: family("nevada.distract") },
    { id: "nevada.notice", kind: "puzzle", chain: "B", title: "Read the notice on the fence", lead: "bigsis", scene: "nevada-roadside", needs: ["nevada.distracted"], sets: "nevada.notice", hint: family("nevada.notice") },
    { id: "nevada.tracks", kind: "gate", title: "Flash the morning sun off the coin onto the place where the tracks stop (and a prayer first)", lead: "family", scene: "nevada-roadside", needs: ["nevada.coinRead", "nevada.notice"], sets: "demo.done", hint: family("nevada.tracks") },
  ],
};

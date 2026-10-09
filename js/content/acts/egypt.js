// Act One: Egypt. The act and its beats (js/content/story.js gathers the acts).
//
// One beat for each row of the puzzle table in docs/PUZZLES-egypt.md. Three things are worth knowing:
//   - "egypt.map" comes before "egypt.reed". Nothing depends on the order; but the Hint button offers the first open
//     beat, and at the very start "I should check what's still in the wagon" is the better thing to hear.
//   - "egypt.topmirror" needs "egypt.knowsLight" as well as the mirror. The goldsmith trades whenever he is offered
//     the sunglasses, so Dad can be holding the copper mirror before he knows what a mirror is for, and the top
//     step will not take it until he does.
//   - a beat's `scene` is the one place it is finished in.
//   - nothing of the family's faith is a beat. Dad's three prayers (the arrival, the dark doorway, the open door), the
//     basket he looks for in the reeds, the bricks and Psalm 90:4 hang on moments and hotspots that were already
//     there, and no puzzle knows of them (docs/PUZZLES-egypt.md, "The family's faith, and the Bible's Egypt").
//   - nor is Lot: the man praying under the palm by the river is Abram's nephew, who tells Dad who he is (Genesis
//     11:27 to 13:5, in his own words) and so when Dad is: Abram is in Egypt this week ("egypt.heardAbram"; the
//     scribe's gossip at the site is the same week from the Egyptian side), and who prays for Dad's boy before they
//     part ("egypt.lotPrayed"). Nor General Feathers, his youngest's stuffed hen, found in his suitcase (`chicken`).
//     A player who talks to people finds the one, and everybody who opens the suitcase finds the other; no puzzle
//     needs either, and the Hint button does not send him to them. Lot still says what the old water carrier said
//     for the puzzles (the boy went up the track; the Horizon; the wall that hums; the scribe's split pen).
//   - nor is the door mirror's glint, and the sun off it in his eyes the first time he comes up to the car
//     ("egypt.dazzled"): the mirror's hint, long before he needs it.
// The chains: A gets him inside. B teaches the rule. C1, C2 and C3 are the three reflectors, in any order.
// The date: about 1920 B.C., by the Bible's own count of years (briefs/DATING.md; docs/CHARACTERS.md, "How the game
// counts the years").

export const act = {
  id: 1, title: "Act One: Scattered", era: "egypt", gate: "egypt.ready",
  summary: "Dad lands by the Nile, alone, about 1920 B.C.: the Egypt of his Bible, though at first he cannot tell when in it. His son's sneaker prints go up to the pyramid that is being finished, where work has stopped because a wall inside has begun to hum. In his suitcase, under the shirts, is his youngest's stuffed hen, General Feathers, sent along to keep an eye on him. The man praying in the shade of a palm by the river, while his donkey drinks, is Lot, Abram's nephew, waiting for the king's men to see his uncle's household out of Egypt; he tells Dad who he is, and so when Dad is (Genesis 12), and before they part he prays for Dad's boy. Dad gets himself onto the scribe's list and past the guard; learns from a lamp boy, and from a flashlight on its last batteries, that light opens the door in the air and more light opens it wider; and brings a sunbeam around three corners, with a windshield shade, a door mirror and a goldsmith's copper mirror, to open it wide enough to walk through.",
  beats: [
    { id: "egypt.arrive", kind: "cutscene", title: "Crash landing by the Nile: small sneaker prints go up the track (and a prayer)", lead: "dad", scene: "egypt-crash", needs: ["seen.intro"], sets: "egypt.arrived" },

    { id: "egypt.map", kind: "puzzle", chain: "A", title: "Take the road map from the glovebox", lead: "dad", scene: "egypt-crash", needs: ["egypt.arrived"], sets: "egypt.hasMap", hint: "hint.egypt.map" },
    { id: "egypt.reed", kind: "puzzle", chain: "A", title: "Cut a reed by the river", lead: "dad", scene: "egypt-crash", needs: ["egypt.arrived"], sets: "egypt.hasReed", hint: "hint.egypt.reed" },
    { id: "egypt.pen", kind: "puzzle", chain: "A", title: "Give the scribe the reed: he can write again", lead: "dad", scene: "egypt-site", needs: ["egypt.hasReed"], sets: "egypt.penGiven", hint: "hint.egypt.pen" },
    { id: "egypt.pass", kind: "puzzle", chain: "A", title: "Give the scribe the map to write on: he writes a pass", lead: "dad", scene: "egypt-site", needs: ["egypt.hasMap", "egypt.penGiven"], sets: "egypt.hasPass", hint: "hint.egypt.mark" },
    { id: "egypt.inside", kind: "puzzle", chain: "A", title: "Show the guard the pass and climb to the entrance", lead: "dad", scene: "egypt-site", needs: ["egypt.hasPass"], sets: "egypt.inside", hint: "hint.egypt.inside" },

    { id: "egypt.witness", kind: "puzzle", chain: "B", title: "Hear from the lamp boy what happened to the small one", lead: "dad", scene: "egypt-gallery", needs: ["egypt.inside"], sets: "egypt.heardBoy", hint: "hint.egypt.witness" },
    { id: "egypt.flash", kind: "puzzle", chain: "B", title: "Shine the flashlight at the wall that hums", lead: "dad", scene: "egypt-chamber", needs: ["egypt.inside"], sets: "egypt.knowsLight", hint: "hint.egypt.flash" },

    { id: "egypt.shade", kind: "puzzle", chain: "C1", title: "Get the guard to hold the windshield shade in the sun, for a root beer", lead: "dad", scene: "egypt-site", needs: ["egypt.knowsLight"], sets: "egypt.shadeSet", hint: "hint.egypt.shade" },
    { id: "egypt.carmirror", kind: "puzzle", chain: "C2", title: "Wedge the wagon's door mirror in the slot at the foot of the gallery", lead: "dad", scene: "egypt-gallery", needs: ["egypt.knowsLight"], sets: "egypt.footSet", hint: "hint.egypt.carmirror" },
    { id: "egypt.trade", kind: "puzzle", chain: "C3", title: "Trade the sunglasses to the goldsmith for his copper mirror", lead: "dad", scene: "egypt-chamber", needs: ["egypt.knowsLight"], sets: "egypt.hasCopper", hint: "hint.egypt.trade" },
    { id: "egypt.topmirror", kind: "puzzle", chain: "C3", title: "Stand the copper mirror on the step at the top of the gallery", lead: "dad", scene: "egypt-gallery", needs: ["egypt.hasCopper", "egypt.knowsLight"], sets: "egypt.topSet", hint: "hint.egypt.topmirror" },

    { id: "egypt.leave", kind: "gate", title: "The sunbeam opens the door wide (and he gives thanks): step up to it (Psalm 90:4)", lead: "dad", scene: "egypt-chamber", needs: ["egypt.shadeSet", "egypt.footSet", "egypt.topSet"], sets: "egypt.ready", hint: "hint.egypt.leave" },
  ],
};

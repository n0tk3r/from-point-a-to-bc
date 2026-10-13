// Act Two: Rome. The story (js/content/story.js) gathers this with the other acts; docs/PUZZLES-rome.md is the act written out.
// One beat for each row of the table in the act's design (briefs/LEVEL-rome.md, and since round thirteen
// briefs/out/rome2-design.md, section 4.2), in the table's order but for the coin's chain, which comes last.
//
// The order matters for hints: the Hint button speaks for the first beat that is open. So he is steered through
// chain A, then chain B, then past the doorkeeper, and only then to the coin (if he has not picked it up on the
// way) and the light. With the coin in the table's place, its hint would be on offer before the hint for getting
// in, and the hint for getting in would never be heard.
// ROME-13S1 (round thirteen, the bigger Rome: briefs/ROME-13.md, "Names everyone shares", the beats; SCENES-13R.md): the
// three new puzzles are beats in their chains. Chain A has the wrong toga (`rome.wrong`, on the steps: the senator finds
// a Gaul's toga), the Gaul (`rome.gaul`, in the Forum) and the right toga (`rome.delivered`); chain B has the keeper's
// boy (`rome.breakfast` now ends when the keeper has said where his boy and the breakfast are) and Juno's geese
// (`rome.geese`, on the Capitol: the breakfast now comes from Titus); and chain C, after the spark, has Phyllis's wish
// (`rome.wish`, `rome.felix`, `rome.granted`), which the toss now waits for. The wish's beats come after the spark for the
// same reason as the coin's after getting in: the wish's hint ("I'm not throwing it through a door without asking") is
// the right one to hear once the door is open, and not before there is a door to throw it through. Every beat is the
// Son's, and the act's gate is still `rome.tossed`.
// Chains A, B and C can be played in any order, and mixed.

export const act = {
  id: 2, title: "Act Two: Meanwhile", era: "rome", gate: "rome.tossed",
  summary: "Rome, the Ides of March, 44 B.C. The door in time has let the Son out inside the temple of Saturn and shut behind him, and the doorkeeper has carried him out. To get back in he must be what the doorkeeper lets in: a boy in a clean tunic, carrying something for the god. He runs a senator's toga up from the laundry, finds it is a Gaul's, and trades it back by showing a lost Gaul in the Forum the way to the Senate; he brings the soothsayer's breakfast down from the Capitol, past Juno's geese, for a box of incense; and before he spends the wish he borrowed from the fountain he asks its owner, a garland seller, and carries her lamp across the Tiber to her son. Inside, he bounces the morning sun off the coin onto the place that hums, and a door opens exactly the size of the coin. He tosses the coin through. It does not come back down.",
  beats: [
    { id: "rome.arrive", kind: "cutscene", title: "Not the rest stop", lead: "son", scene: "rome-steps", needs: ["egypt.ready"], sets: "rome.arrived" },

    { id: "rome.toga", kind: "puzzle", chain: "A", title: "Take the senator's clean toga from the washerwoman", lead: "son", scene: "rome-street", needs: ["rome.arrived"], sets: "rome.hasToga", hint: "hint.rome.toga" },
    { id: "rome.wrong", kind: "puzzle", chain: "A", title: "Deliver it: it is not his toga", lead: "son", scene: "rome-steps", needs: ["rome.hasToga"], sets: "rome.wrongToga", hint: "hint.rome.delivered" },
    { id: "rome.gaul", kind: "puzzle", chain: "A", title: "Show the Gaul the way, and swap togas", lead: "son", scene: "rome-forum", needs: ["rome.wrongToga"], sets: "rome.swapped", hint: "hint.rome.gaul" },
    { id: "rome.delivered", kind: "puzzle", chain: "A", title: "Deliver the right toga to the senator", lead: "son", scene: "rome-steps", needs: ["rome.swapped"], sets: "rome.delivered", hint: "hint.rome.delivered2" },
    { id: "rome.tunic", kind: "puzzle", chain: "A", title: "Go back for the tunic she promised", lead: "son", scene: "rome-street", needs: ["rome.delivered"], sets: "rome.hasTunic", hint: "hint.rome.tunic" },

    { id: "rome.breakfast", kind: "puzzle", chain: "B", title: "Ask the keeper for the soothsayer's breakfast", lead: "son", scene: "rome-street", needs: ["rome.arrived"], sets: "rome.knowsBoy", hint: "hint.rome.breakfast" },
    { id: "rome.geese", kind: "puzzle", chain: "B", title: "Get the keeper's boy, and the breakfast, away from Juno's geese", lead: "son", scene: "rome-capitol", needs: ["rome.knowsBoy"], sets: "rome.hasBreakfast", hint: "hint.rome.geese" },
    { id: "rome.incense", kind: "puzzle", chain: "B", title: "Feed the soothsayer, and be trusted with his incense", lead: "son", scene: "rome-steps", needs: ["rome.hasBreakfast"], sets: "rome.hasIncense", hint: "hint.rome.incense" },

    { id: "rome.inside", kind: "puzzle", chain: "A+B", title: "Past the doorkeeper: in the tunic, with the incense", lead: "son", scene: "rome-steps", needs: ["rome.hasTunic", "rome.hasIncense"], sets: "rome.inside", hint: "hint.rome.inside" },

    { id: "rome.coin", kind: "puzzle", chain: "C", title: "Borrow a wish from the fountain", lead: "son", scene: "rome-street", needs: ["rome.arrived"], sets: "rome.hasCoin", hint: "hint.rome.coin" },
    { id: "rome.spark", kind: "puzzle", chain: "C", title: "Bounce the sunlight off the coin onto the place that hums", lead: "son", scene: "rome-temple", needs: ["rome.inside", "rome.hasCoin"], sets: "rome.doorOpen", hint: "hint.rome.spark" },
    { id: "rome.wish", kind: "puzzle", chain: "C", title: "Ask Phyllis about her wish, and take her lamp to her son", lead: "son", scene: "rome-forum", needs: ["rome.hasCoin"], sets: "rome.hasLamp", hint: "hint.rome.wish" },
    { id: "rome.felix", kind: "puzzle", chain: "C", title: "Find Felix at the barges across the Tiber", lead: "son", scene: "rome-tiber", needs: ["rome.hasLamp"], sets: "rome.felixWord", hint: "hint.rome.felix" },
    { id: "rome.granted", kind: "puzzle", chain: "C", title: "Tell Phyllis; she lets him keep the coin", lead: "son", scene: "rome-forum", needs: ["rome.felixWord"], sets: "rome.wishGranted", hint: "hint.rome.granted" },

    { id: "rome.toss", kind: "gate", title: "Toss the coin through the door", lead: "son", scene: "rome-temple", needs: ["rome.doorOpen", "rome.wishGranted"], sets: "rome.tossed", hint: "hint.rome.toss" },
  ],
};

// Act Two: Rome. The story (js/content/story.js) gathers this with the other acts; docs/PUZZLES-rome.md is the act written out.
// One beat for each row of the table in the act's design (briefs/LEVEL-rome.md), in the table's order but for one:
// `rome.coin` comes after `rome.inside` here.
//
// The order matters for hints: the Hint button speaks for the first beat that is open. So he is steered through
// chain A, then chain B, then past the doorkeeper, and only then to the coin (if he has not picked it up on the
// way) and the light. With the coin in the table's place, its hint would be on offer before the hint for getting
// in, and the hint for getting in would never be heard.
// Chains A, B and C can be played in any order, and mixed.

export const act = {
  id: 2, title: "Act Two: Meanwhile", era: "rome", gate: "rome.tossed",
  summary: "Rome, the Ides of March, 44 B.C. The door in time has let the Son out inside the temple of Saturn and shut behind him, and the doorkeeper has carried him out. To get back in he must be what the doorkeeper lets in: a boy in a clean tunic, carrying something for the god. He runs a senator's toga up from the laundry for the loan of a tunic, and a soothsayer's breakfast up from the snack bar for a box of incense. Inside, he bounces the morning sun off a new silver coin onto the place that hums, and a door opens exactly the size of the coin. He tosses the coin through. It does not come back down.",
  beats: [
    { id: "rome.arrive", kind: "cutscene", title: "Not the rest stop", lead: "son", scene: "rome-steps", needs: ["egypt.ready"], sets: "rome.arrived" },

    { id: "rome.toga", kind: "puzzle", chain: "A", title: "Take the senator's clean toga from the washerwoman", lead: "son", scene: "rome-street", needs: ["rome.arrived"], sets: "rome.hasToga", hint: "hint.rome.toga" },
    { id: "rome.delivered", kind: "puzzle", chain: "A", title: "Deliver the toga to the senator", lead: "son", scene: "rome-steps", needs: ["rome.hasToga"], sets: "rome.delivered", hint: "hint.rome.delivered" },
    { id: "rome.tunic", kind: "puzzle", chain: "A", title: "Go back for the tunic she promised", lead: "son", scene: "rome-street", needs: ["rome.delivered"], sets: "rome.hasTunic", hint: "hint.rome.tunic" },

    { id: "rome.breakfast", kind: "puzzle", chain: "B", title: "Take the soothsayer's breakfast from the snack bar", lead: "son", scene: "rome-street", needs: ["rome.arrived"], sets: "rome.hasBreakfast", hint: "hint.rome.breakfast" },
    { id: "rome.incense", kind: "puzzle", chain: "B", title: "Feed the soothsayer, and be trusted with his incense", lead: "son", scene: "rome-steps", needs: ["rome.hasBreakfast"], sets: "rome.hasIncense", hint: "hint.rome.incense" },

    { id: "rome.inside", kind: "puzzle", chain: "A+B", title: "Past the doorkeeper: in the tunic, with the incense", lead: "son", scene: "rome-steps", needs: ["rome.hasTunic", "rome.hasIncense"], sets: "rome.inside", hint: "hint.rome.inside" },

    { id: "rome.coin", kind: "puzzle", chain: "C", title: "Borrow a wish from the fountain", lead: "son", scene: "rome-street", needs: ["rome.arrived"], sets: "rome.hasCoin", hint: "hint.rome.coin" },

    { id: "rome.spark", kind: "puzzle", chain: "C", title: "Bounce the sunlight off the coin onto the place that hums", lead: "son", scene: "rome-temple", needs: ["rome.inside", "rome.hasCoin"], sets: "rome.doorOpen", hint: "hint.rome.spark" },

    { id: "rome.toss", kind: "gate", title: "Toss the coin through the door", lead: "son", scene: "rome-temple", needs: ["rome.doorOpen"], sets: "rome.tossed", hint: "hint.rome.toss" },
  ],
};

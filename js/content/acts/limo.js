// Act Five: Everybody's Grandpa (NEVADA-12SC: new in round twelve). The inside of a gray limousine, driving: the first part
// of the game played by somebody who is not family, and the first part played by a raccoon. GRANDPA JOE can talk to
// anybody and has his hands tied; RANGER cannot talk and has paws. A beat carries one hint for each of them, and Ranger's
// is a list: his "...", and then what Grandpa Joe says he means.
// The design is briefs/out/nevada-expansion-design.md ("Cut-Scene: Backup", "Act Five opens: Everybody's Grandpa"); the
// lines are js/content/lines/nevada.en.js (the cut-scene) and lines/limo.en.js (the rest).
//
// The act opens on the roadside, where Act Four closes: the family has gone through the door, and the man in gray makes a
// phone call he will regret (the cut-scene "Backup", js/content/cutscenes/backup.js). Then the limousine
// (js/content/scenes/nevada-limo.js): "Meanwhile, in a limousine" as it is first entered, Ranger's Ropes (#14), Jed's
// Lunch (#15), and the gate: the limousine slows at the gate of a very small building with a very long name, and the card
// "THE OFFICE OF PECULIAR SECTORS", "Desert Field Headquarters, the same afternoon" (SCENES-17: the act goes on into the
// Office, js/content/acts/office.js, whose "Going Down" is the end of the demo now).

const BOTH = ["grandpajoe", "ranger"];

export const act = {
  id: 5, title: "Act Five: Everybody's Grandpa", era: "nevada", gate: "limo.done",
  summary: "The middle of Nevada, the same morning, after the family has gone through the door. The man in gray calls for a cheeseburger and backup; Grandpa Joe lets the sun shade down, and the door folds shut; and he brings his banjo down on the man in gray's head, once. A gray limousine, four polite men in gray, a clipboard, a length of regulation rope tied in a bow: they carry him off, and Ranger the raccoon runs in after him. In the back of the limousine, driving, Grandpa Joe and Ranger are the leads. Grandpa Joe hums the Last Stop Rag until the men in front put the divider up and keep it up, and Ranger chews through the ropes a strand at a time, sitting on his work whenever a suit looks back. With his hands free Grandpa Joe reads the office's clipboard and eats the cheeseburger that came with the backup: a map of three sealed sectors, and a column for what opens them, blank. Ranger puts the map in his bib pocket, a receipt for the banjo comes back through the divider, and the limousine slows at the gate of the Office Of Peculiar Sectors.",
  beats: [
    { id: "nevada.backup", kind: "cutscene", title: "Backup", lead: BOTH, scene: "nevada-roadside", needs: ["nevada.left"], sets: "nevada.backup" },
    { id: "limo.arrive", kind: "cutscene", title: "Meanwhile, in a limousine", lead: BOTH, scene: "nevada-limo", needs: ["nevada.backup"], sets: "limo.arrived" },
    { id: "limo.ropes", kind: "puzzle", chain: "A", title: "Ranger's Ropes: Grandpa Joe sings, so that nobody looks back, and Ranger chews", lead: BOTH, scene: "nevada-limo", needs: ["limo.arrived"], sets: "limo.loose",
      hint: { grandpajoe: "hint.limo.ropes.joe", ranger: ["limo.ranger.dots", "hint.limo.ropes.ranger"] } },
    { id: "limo.bag", kind: "puzzle", chain: "A", title: "Jed's Lunch: read the clipboard, eat the cheeseburger, keep the map", lead: BOTH, scene: "nevada-limo", needs: ["limo.loose"], sets: "limo.map",
      hint: { grandpajoe: "hint.limo.bag.joe", ranger: ["limo.ranger.dots", "hint.limo.bag.ranger"] } },
    { id: "limo.end", kind: "gate", title: "The gate of the Office Of Peculiar Sectors", lead: BOTH, scene: "nevada-limo", needs: ["limo.map"], sets: "limo.done" },      // (SCENES-17: no longer the end of the demo)
  ],
};

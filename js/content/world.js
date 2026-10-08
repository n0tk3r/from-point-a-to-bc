// Who and what is in the game.
// docs/CHARACTERS.md says who the family are; the puzzle documents in docs/ say what each act is.

/** Everyone who speaks. `color` is the color of their words on screen.
    `sprite` names their figure in js/art/people.js, where their looks are set.
    `lead: true` marks someone the player can control: they get a place and pockets of their own.
    `keeps` is what those pockets are called on screen ("Mom's handbag"). */
export const cast = {
  dad:      { name: "Dad", color: "#ffd34d", sprite: "dad", lead: true, keeps: "pockets" },
  son:      { name: "Son", color: "#7fe3ff", sprite: "son", lead: true, keeps: "backpack" },
  mom:      { name: "Mom", color: "#8ff0c0", sprite: "mom", lead: true, keeps: "handbag" },
  bigsis:   { name: "Big Sister", color: "#c3b8ff", sprite: "bigsis", lead: true, keeps: "pockets" },
  lilsis:   { name: "Little Sister", color: "#ff9ec4", sprite: "lilsis", lead: true, keeps: "pockets" },
  // Egypt (their words are tints nobody else in the game uses, and each stands clear of Dad's yellow)
  scribe:   { name: "Scribe", color: "#ffb48a", sprite: "scribe" },
  carrier:  { name: "Water Carrier", color: "#6fd6c4", sprite: "carrier" },
  overseer: { name: "Overseer", color: "#ff8c69", sprite: "overseer" },
  hauler1:  { name: "Hauler", color: "#c8dc6a", sprite: "hauler1" },
  hauler2:  { name: "Hauler", color: "#c8dc6a", sprite: "hauler2" },
  hauler3:  { name: "Hauler", color: "#c8dc6a", sprite: "hauler3" },
  guard:    { name: "Guard", color: "#8db3f5", sprite: "guard" },
  lampboy:  { name: "Lamp Boy", color: "#eaa2f0", sprite: "lampboy" },
  goldsmith: { name: "Goldsmith", color: "#9ad98f", sprite: "goldsmith" },
  // Rome (each stands clear of the Son's blue)
  keeper:   { name: "Snack-Bar Keeper", color: "#ffa64d", sprite: "keeper" },
  washer:   { name: "Washerwoman", color: "#b4e070", sprite: "washer" },
  urchin:   { name: "Street Boy", color: "#f2e86b", sprite: "urchin" },
  soothsayer: { name: "Soothsayer", color: "#b8c4a6", sprite: "soothsayer" },
  senator:  { name: "Senator", color: "#c98ae0", sprite: "senator" },
  doorkeeper: { name: "Doorkeeper", color: "#c9b08a", sprite: "doorkeeper" },
  clerk:    { name: "Clerk", color: "#e0b0a4", sprite: "clerk" },
  dateseller: { name: "Date Seller", color: "#e9c46a", sprite: "dateseller" },
  // Nevada
  oldtimer: { name: "Old-Timer", color: "#e6d3a0", sprite: "oldtimer" },
  agent:    { name: "Man in Gray", color: "#c9ced6", sprite: "agent" },
  narrator: { name: "Narrator", color: "#f6e3b8" },
};

/** Time periods. The id matches a palette in css/tokens.css and a track in sound.js. */
export const eras = {
  present: { name: "The present", date: "", music: "road" },
  egypt:   { name: "Ancient Egypt", date: "about 1920 B.C.", music: "egypt" },      // by the Bible's own count of years (Ussher): see docs/CHARACTERS.md, "How the game counts the years"
  rome:    { name: "Rome", date: "44 B.C.", music: "rome" },
  home:    { name: "Home", date: "The present", music: "home" },
  nevada:  { name: "The Middle of Nevada", date: "The next morning", music: "nevada" },
  tunnel:  { name: "Between whens", date: "", music: "tunnel" },
};

/** Things that can be carried. `icon` is a painted picture in art/items/. `look` is a line ID, or one for each lead who might be holding it. */
export const items = {
  // Act One: Dad's
  reed:         { name: "reed", icon: "reed.png", look: "item.reed.look" },
  map:          { name: "road map", icon: "map.png", look: "item.map.look" },
  pass:         { name: "work pass", icon: "pass.png", look: "item.pass.look" },
  flashlight:   { name: "flashlight", icon: "flashlight.png", look: "item.flashlight.look" },
  rootbeer:     { name: "root beer", icon: "rootbeer.png", look: "item.rootbeer.look" },
  shade:        { name: "windshield shade", icon: "shade.png", look: "item.shade.look" },
  carmirror:    { name: "door mirror", icon: "carmirror.png", look: "item.carmirror.look" },
  sunglasses:   { name: "sunglasses", icon: "sunglasses.png", look: "item.sunglasses.look" },
  coppermirror: { name: "copper mirror", icon: "coppermirror.png", look: "item.coppermirror.look" },
  chicken:      { name: "General Feathers", icon: "chicken.png", look: "item.chicken.look" },    // Little Sister's stuffed chicken, sent along to keep an eye on him
  // Act Two: the Son's
  toga:      { name: "senator's toga", icon: "toga.png", look: "item.toga.look" },
  tunic:     { name: "small tunic", icon: "tunic.png", look: "item.tunic.look" },
  breakfast: { name: "soothsayer's breakfast", icon: "breakfast.png", look: "item.breakfast.look" },
  incense:   { name: "incense box", icon: "incense.png", look: "item.incense.look" },
  phone:     { name: "dead phone", icon: "phone.png", look: "item.phone.look" },
  quarter:   { name: "quarter", icon: "quarter.png", look: "item.quarter.look" },
  gum:       { name: "pack of gum", icon: "gum.png", look: "item.gum.look" },
  // The coin goes on from the Son to Mom and the girls, so each of them has a line for it.
  coin: { name: "silver coin", icon: "coin.png", look: { son: "item.coin.look", mom: "item.coin.mom", bigsis: "item.coin.bigsis", lilsis: "item.coin.lilsis", any: "item.coin.look" } },
  // Act Three: each of the three has her own line for each thing
  note: { name: "sticky note", icon: "note.png", look: { mom: "item.note.mom", bigsis: "item.note.bigsis", lilsis: "item.note.lilsis", any: "item.note.mom" } },
  studykey: { name: "study key", icon: "studykey.png", look: { mom: "item.studykey.mom", bigsis: "item.studykey.bigsis", lilsis: "item.studykey.lilsis", any: "item.studykey.mom" } },
  lilflash: { name: "pink flashlight", icon: "lilflash.png", look: { mom: "item.lilflash.mom", bigsis: "item.lilflash.bigsis", lilsis: "item.lilflash.lilsis", any: "item.lilflash.lilsis" } },
  pencil: { name: "Dad's pencil", icon: "pencil.png", look: { mom: "item.pencil.mom", bigsis: "item.pencil.bigsis", lilsis: "item.pencil.lilsis", any: "item.pencil.mom" } },
  carkey: { name: "spare car key", icon: "carkey.png", look: { mom: "item.carkey.mom", bigsis: "item.carkey.bigsis", lilsis: "item.carkey.lilsis", any: "item.carkey.mom" } },
  batteries: { name: "batteries", icon: "batteries.png", look: { mom: "item.batteries.mom", bigsis: "item.batteries.bigsis", lilsis: "item.batteries.lilsis", any: "item.batteries.bigsis" } },
};

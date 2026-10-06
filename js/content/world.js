// Who and what is in the game.
// PLACEHOLDER CONTENT: names, eras and dates here exist to prove the engine.
// Replace them as the puzzle document is written. docs/CHARACTERS.md says who these people are.

/** Everyone who speaks. `color` is the color of their words on screen.
    `sprite` names their figure in js/art/people.js, where their looks are set.
    `lead: true` marks someone the player can control: they get a place and pockets of their own. */
export const cast = {
  dad:      { name: "Dad", color: "#ffd34d", sprite: "dad", lead: true },
  son:      { name: "Son", color: "#7fe3ff", sprite: "son", lead: true },
  mom:      { name: "Mom", color: "#8ff0c0", sprite: "mom", lead: true },
  bigsis:   { name: "Big Sister", color: "#c3b8ff", sprite: "bigsis", lead: true },
  lilsis:   { name: "Little Sister", color: "#ff9ec4", sprite: "lilsis", lead: true },
  scribe:   { name: "Scribe", color: "#ffb48a", sprite: "scribe" },
  oldtimer: { name: "Old-Timer", color: "#e6d3a0", sprite: "oldtimer" },
  agent:    { name: "Man in Gray", color: "#c9ced6", sprite: "agent" },
  narrator: { name: "Narrator", color: "#f6e3b8" },
};

/** Time periods. The id matches a palette in css/tokens.css and a track in sound.js. */
export const eras = {
  present: { name: "The present", date: "", music: "road" },
  egypt:   { name: "Ancient Egypt", date: "1250 B.C.", music: "egypt" },
  rome:    { name: "Rome", date: "44 B.C.", music: "rome" },
  home:    { name: "Home", date: "The present", music: "home" },
  nevada:  { name: "The Middle of Nevada", date: "The next morning", music: "nevada" },
  tunnel:  { name: "Between whens", date: "", music: "tunnel" },
};

/** Things that can be carried. `look` is a line ID, or one for each lead who might be holding it. */
export const items = {
  map:  { name: "road map", icon: "map", look: "item.map.look" },
  reed: { name: "reed", icon: "reed", look: "item.reed.look" },
  coin: { name: "silver coin", icon: "coin", look: { son: "item.coin.look", mom: "item.coin.mom", bigsis: "item.coin.bigsis", lilsis: "item.coin.lilsis", any: "item.coin.look" } },
  note: { name: "sticky note", icon: "note", look: { mom: "item.note.mom", bigsis: "item.note.bigsis", lilsis: "item.note.lilsis", any: "item.note.mom" } },
};

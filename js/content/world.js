// Who and what is in the game.
// PLACEHOLDER CONTENT: names, eras and dates here exist to prove the engine.
// Replace them as the character bibles and the puzzle document are written.

/** Everyone who speaks. `color` is the colour of their words on screen. */
export const cast = {
  dad:      { name: "Dad", color: "#ffd34d", sprite: "dad", lead: true },
  son:      { name: "Son", color: "#7fe3ff", sprite: "son", lead: true },
  scribe:   { name: "Scribe", color: "#ffb48a", sprite: "scribe" },
  narrator: { name: "Narrator", color: "#f6e3b8" },
};

/** Time periods. The id matches a palette in css/tokens.css and a track in sound.js. */
export const eras = {
  present: { name: "The present", date: "", music: "road" },
  egypt:   { name: "Ancient Egypt", date: "1250 B.C.", music: "egypt" },
  rome:    { name: "Rome", date: "44 B.C.", music: "rome" },
  tunnel:  { name: "Between whens", date: "", music: "tunnel" },
};

/** Things that can be carried. `look` is a line ID. */
export const items = {
  map:  { name: "road map", icon: "map", look: "item.map.look" },
  reed: { name: "reed", icon: "reed", look: "item.reed.look" },
  coin: { name: "coin", icon: "coin", look: "item.coin.look" },
};

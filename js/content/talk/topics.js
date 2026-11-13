// TALK-24: topics in a dialogue tree (js/engine/dialogue.js talk(); docs/DESIGN.md, section 7, "Dialogue trees").
// The author, 10 November: "There are way too many dialogue choices in Japan. Usually in point and click adventure games,
// dialogues have trees so if you choose to talk about a topic it takes them down a certain tree/option." So a menu shows
// four topics and a goodbye at most: the questions on one subject go in a node of their own, opened by a topic option (said
// by whoever asks it) and left by a way back (said by whoever is being played). Every question is the one it was, under the
// same id, so what a save remembers of a talk is unchanged.
//
//   topic("lore", "edo.denzo.topic.lore.big", "lore")     an option that opens the node "lore": it shows only while something
//                                                         in that node would (an empty topic is never offered), and is
//                                                         marked new while anything in it is new
//   back("lore")                                          the way back to the menu before, said by whoever is being played
//   back("lore", "talk.back.son")                         ... or by someone in particular (the Son, through the door)

/** The way back's words: whoever is being played (js/content/lines/common.en.js, `talk.back.*`). */
export const backLine = (g) => `talk.back.${(g.store && g.store.data && g.store.data.active) || "mom"}`;

/** An option that opens another node of the tree as a topic. `more`: anything else the option needs (a `when`, say). */
export const topic = (id, line, node, more = {}) => ({ id, line, topic: true, then: node, ...more });

/** The way back out of a topic. Its id is the topic node's, so that every way back in a tree is its own. */
export const back = (node, line = backLine) => ({ id: `${node}.back`, line, then: "back" });

/** TALK-24: a topic in a scene's own menu (a loop of g.choose with { talk: true }, not a tree). The menu before it shows the
    topic as { id, line, under: options } (it stays while anything under it would show, and is marked new while anything in
    it is); picked, the script says its line and calls this, which asks the topic's options, each answered by `answer(id)`,
    until the way back is picked or nothing is left in it. */
export async function askAbout(g, options, answer, line = backLine(g)) {
  for (;;) {
    if (!options.some((o) => (!o.when || o.when(g)) && g.dialogue.stays(o))) return;          // nothing left: back by itself
    const pick = await g.choose([...options, { id: "back", line, exit: true, asked: 1 }], { talk: true });
    if (pick == null || pick === "back") { if (pick === "back") await g.say(line); return; }
    await answer(pick);
  }
}

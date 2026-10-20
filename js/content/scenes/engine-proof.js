// The worked example of a painted scene: where the wagon came down, by the Nile.
//
// A painted scene is a backdrop picture and a few cut-outs, plus the numbers that let
// people walk about in it. Every number in this file is a pixel on the 800x600 picture,
// so it can be measured straight off the painting.
//
//   picture   the backdrop: everything that is far away or flat on the ground
//   planes    painted cut-outs: PNG files the size of the whole picture with a clear
//             background, laid over it at (0, 0). The engine sorts them with the people.
//   walk      the outline of the ground people can stand on
//   horizon, full   how people shrink as they walk away (see below)
//
// Try it: index.html?scene=engine-proof&lead=dad     (hold H to see an outline round everything that can be clicked)
// This scene is not part of the story. It stays as the pattern to copy, the way
// sketch-example.js is the pattern for a scene that has no painting yet.

import { scaleAt } from "../../engine/walk.js";          // ROME-13E: the size of a row, for the man who comes down from his window

const art = "art/scenes/egypt-crash/";
const fx = (g) => !!g.flag("proof.fx");          // the things that move by nature (`fx`, below) are on the stage while this is true

// ---------- LETTERBOX-11: the letterbox, the engine's own proof of it (docs/DESIGN.md, "The letterbox") ----------
// On the stage while "proof.letterbox" is true: index.html?scene=engine-proof&lead=dad&flags=proof.letterbox.
// Dad is here with a pack of gum, and the Son is in another century (the market street sketch, in Rome), so the two are
// a team and switching to him is the Timer and his map (MAP-15, below; before, the short tunnel). A small door in time hangs in the air over the sand. Anything small
// that whoever is here carries can be put in it for the one at the other end (this scene's own choice, SMALL: the engine
// never decides what fits), and it waits in the tunnel, marking that person's portrait, until they take it out of a door
// of theirs. The sketch has no door, so the proof lets the Son take it out of this one: come back here as the Son
// (switch again) and on arrival the door gives it up (g.arrive, a word, g.receive). The door with nothing in hand is a
// word through it with whoever is at the other end: g.through, and a choose through the door.
// MAP-15: the two scenes are on two sketch maps of the proof's own (js/content/maps.js: "proof-sand", in Egypt, and
// "proof-street", in Rome), so switching to the Son is the Timer turning from B.C. to the middle notch (four notches, a
// click at each and the bell), then the street's map with the Son breathing; a click on him (or Enter) drops into his
// scene, and Esc goes back with nothing changed. To see it: index.html?scene=engine-proof&lead=dad&flags=proof.letterbox,proof.arrived,
// then press 2.
const letterbox = (g) => !!g.flag("proof.letterbox");
const DOOR = [360, 436];                                                        // the middle of the small door, in the air over the sand (its foot is row 470)
const OTHER = { dad: "son", son: "dad" };                                       // who is at the other end, for whoever is here
const SMALL = ["gum", "coin", "quarter", "map", "note", "pencil", "batteries", "studykey", "carkey", "reed", "pass", "sunglasses"];   // what fits through
const mine = (g, dad, son) => (g.store.data.active === "son" ? son : dad);      // the line for whoever is here
// The lines are the proof's own, for the tests: added to the game's lines as the scene is built (setup), since no act owns them.
const LINES = {
  "proof.door.look": ["dad", "A small door in time. Letterbox-sized. The kind you post things through, not people."],
  "proof.door.look.son": ["son", "A tiny door in time. If I were a hamster I'd be through it already."],
  "proof.door.put": ["dad", "In it goes. Special delivery, two thousand years express."],
  "proof.door.put.son": ["son", "Posting it. No stamp. Let's see if time charges postage."],
  "proof.door.gone": ["dad", "And it's gone. Somewhere. Somewhen."],
  "proof.door.gone.son": ["son", "Gone! That is the best mailbox I have ever seen."],
  "proof.door.came": ["dad", "Something's come through. From the Son, I'd guess. It has his fingerprints on it."],
  "proof.door.came.son": ["son", "Whoa. Something just came through the door for me. Time mail!"],
  "proof.door.hello": ["dad", "Hello? Anyone at the other end?"],
  "proof.door.hello.son": ["son", "Dad? Dad! Are you in there? Say something old."],
  "proof.door.answer.1": ["son", "Dad? Is that YOU? You sound like you're inside a drainpipe."],
  "proof.door.answer.2": ["son", "I'm in a street. It's made of rectangles. Nobody here has heard of lunch."],
  "proof.door.answer.dad": ["dad", "I'm here, buddy. Speak up: this door has a lot of centuries in it."],
  "proof.door.son.fine": ["son", "I'm fine. Really. The rectangles are very friendly."],
  "proof.door.son.send": ["son", "Send me something! Anything! A snack would be ideal!"],
  "proof.door.son.bye": ["son", "Gotta go. Someone's trying to sell me a rectangle."],
  "proof.door.fine": ["dad", "Rectangles. Right. Stay put, buddy."],
  "proof.door.send": ["dad", "I'll see what fits through. No promises about snacks."],
  "proof.door.bye": ["dad", "Don't buy anything. We don't have the exchange rate."],
  // TALK-11: the water carrier's talk (the tree is CARRIER, below)
  "proof.carrier.look": ["dad", "An old man with a water-skin, in no hurry at all. Somebody around here has the right idea."],
  "proof.carrier.hello.1": ["carrier", "Peace, stranger. You came down in the big wooden thing?"],
  "proof.carrier.hello.2": ["carrier", "I carry water. Up to the stone, down to the river, up to the stone. Forty years. Ask me anything about either."],
  "proof.carrier.opt.jars": ["dad", "What's in the jars?"],
  "proof.carrier.jars.1": ["carrier", "Water."],
  "proof.carrier.jars.2": ["carrier", "Still water. It was water the first time you asked, too."],
  "proof.carrier.jars.more": ["carrier", "Stranger, I am going to tell you a secret. It is water."],
  "proof.carrier.opt.river": ["dad", "Tell me about the river."],
  "proof.carrier.river.1": ["carrier", "The river. She rises, she falls, she feeds everybody and she drowns a few. Like a mother, my wife says."],
  "proof.carrier.opt.fish": ["dad", "Any fish in it?"],
  "proof.carrier.fish.1": ["carrier", "Fish, yes. Also crocodiles. The fish are for eating. The crocodiles have the same idea about you."],
  "proof.carrier.opt.show": ["dad", "Show me where you fill up."],
  "proof.carrier.show.1": ["carrier", "Come. Watch the water, not the view."],
  "proof.carrier.show.2": ["carrier", "Here. Upstream of the donkey. That is the whole art of it."],
  "proof.carrier.opt.enough": ["dad", "That's enough about fish."],
  "proof.carrier.enough": ["carrier", "Nobody ever says that about water."],
  "proof.carrier.opt.swim": ["dad", "Can I swim in it?"],
  "proof.carrier.swim.1": ["carrier", "You can. Once."],
  "proof.carrier.opt.back": ["dad", "Never mind the river."],
  "proof.carrier.opt.name": ["dad", "What do they call you?"],
  "proof.carrier.name.1": ["carrier", "Water Carrier. Before that, Boy. If I live, Old Water Carrier."],
  "proof.carrier.name.2": ["carrier", "And you are the man who fell out of the sky in a wooden box. Nobody will need to ask twice."],
  "proof.carrier.opt.pyramid": ["dad", "Who's the big pointy one for?"],
  "proof.carrier.pyramid.1": ["carrier", "The king. He is in no hurry either. His sons are."],
  "proof.carrier.opt.bye": ["dad", "I'll let you get on."],
  "proof.carrier.bye": ["carrier", "Get on. Yes. Up to the stone, down to the river. Mind the crocodiles, sky-man."],
  // NEVADA-12E: the painted creature (CRITTER, below), the party of two and the strip
  "proof.critter.dots": ["critter", "..."],
  "proof.critter.look": ["dad", "A small grey creature in a black mask, turning a pebble over in its hands. Either a raccoon or a very small bandit."],
  "proof.critter.hello.dad": ["dad", "He says hello. I think. It was a very warm '...'."],
  "proof.critter.opt.what": ["dad", "What are you, exactly?"],
  "proof.critter.what.dad": ["dad", "He says he is painted. Frame by frame, by hand. He seems proud of it."],
  "proof.critter.opt.join": ["dad", "Want to come along?"],
  "proof.critter.join.dad": ["dad", "That was a yes. I am now on a team with a creature in a mask."],
  "proof.critter.opt.bye": ["dad", "See you around, little bandit."],
  "proof.critter.given.dad": ["dad", "He says thank you. It goes in the stash. Everything goes in the stash."],
  "proof.critter.shades.dad": ["dad", "And on they go. He wears them better than I did."],
  "proof.cooler.look": ["dad", "The cooler. It fell off the roof in the landing. Nothing in it but ice that has given up."],
  "proof.cooler.use.dad": ["dad", "There's nothing in it for me. There might be something in it for somebody with smaller hands."],
  "proof.critter.nibble.dad": ["dad", "He's chewing the lid. That cooler has been through enough today."],
  "proof.talk.dad.critter.1": ["dad", "How's the stash coming along?"],
  "proof.talk.dad.critter.1b": ["dad", "Full, he says. Of pebbles. Mostly pebbles."],
  "proof.talk.critter.dad.1": ["dad", "Yes, all right. I'll carry the heavy things. You carry the pebbles."],
  "proof.hint.party.dad": ["dad", "Somebody should get into that cooler. Somebody with small hands and no manners. Not me."],
  "proof.hint.party.critter.dad": ["dad", "He says the cooler is his job and I'm in the way."],
};

// ---------- TALK-11: a dialogue tree, the engine's own proof of it (docs/DESIGN.md, "Dialogue trees") ----------
// On the stage while "proof.talk" is true: index.html?scene=engine-proof&lead=dad&flags=proof.talk. An old water carrier
// stands on the sand by the river; talking to him is `g.talk(CARRIER)`. (TALK-18: the jars and "show me" are its clues: they stay, asked again.) The tree below uses every piece there is: a start
// that depends on the story (`start` as a function: his greeting once, then straight to the questions), a node with four
// ways in, a fork two deep (the river, then the fish), an option gated by `when` that appears only after another was
// picked (the pyramid, after his name), a `once` (his name), a reply keyed by the nth asking with `more` (the jars), a
// `set` (his name), an async `do` (he walks to the water and back), `back`, `root`, and an exit that is a line.
const talk = (g) => !!g.flag("proof.talk");
const CARRIER_AT = [250, 480];                                                  // where he stands
/** He shows Dad where he fills up: down to the water's edge, a word there, and back to his place. (A `do` script: run after the option's lines, and awaited.) */
async function fetchWater(g) {
  await g.moveTo(200, 455, "carrier");
  await g.say("proof.carrier.show.2");
  await g.moveTo(CARRIER_AT[0], CARRIER_AT[1], "carrier");
  const he = g.actor("carrier");
  if (he) he.face("E");
}
const CARRIER = {
  id: "proof.carrier",
  start: (g) => (g.flag("proof.carrierMet") ? "ask" : "hello"),
  nodes: {
    hello: { say: ["proof.carrier.hello.1", "proof.carrier.hello.2"], then: (g) => { g.flag("proof.carrierMet", true); return "ask"; } },
    ask: {
      options: [
        { id: "jars", line: "proof.carrier.opt.jars", clue: true, say: { 1: ["proof.carrier.jars.1"], 2: ["proof.carrier.jars.2"], more: ["proof.carrier.jars.more"] } },
        { id: "river", line: "proof.carrier.opt.river", say: ["proof.carrier.river.1"], then: "river" },
        { id: "name", line: "proof.carrier.opt.name", once: true, say: ["proof.carrier.name.1", "proof.carrier.name.2"], set: "proof.carrierNamed" },
        { id: "pyramid", line: "proof.carrier.opt.pyramid", when: (g) => g.asked("proof.carrier/name") > 0, say: ["proof.carrier.pyramid.1"] },
        { id: "bye", line: "proof.carrier.opt.bye", say: ["proof.carrier.bye"], then: "exit" },
      ],
    },
    river: {
      options: [
        { id: "fish", line: "proof.carrier.opt.fish", then: "fish" },
        { id: "swim", line: "proof.carrier.opt.swim", say: ["proof.carrier.swim.1"] },
        { id: "riverback", line: "proof.carrier.opt.back", then: "back" },
      ],
    },
    fish: {
      say: ["proof.carrier.fish.1"],
      options: [
        { id: "show", line: "proof.carrier.opt.show", clue: true, say: ["proof.carrier.show.1"], do: fetchWater, then: "back" },
        { id: "enough", line: "proof.carrier.opt.enough", say: ["proof.carrier.enough"], then: "root" },
      ],
    },
  },
};

// ---------- NEVADA-12E: a lead drawn from painted frames, the engine's own proof of it (docs/DESIGN.md, section 4, "Painted frame by frame") ----------
// On the stage while "proof.painted" is true: index.html?scene=engine-proof&lead=dad&flags=proof.painted. A small creature of
// the engine's own (art/proof/critter-*.png, painted by a script, its sidecar art/proof/critter.json, `critter` in
// js/art/painted.js and in world.js) sits up on the sand, one of the scene's people with a life of his own: his small
// movements are sets of his frames (he looks round at us; he turns a pebble over in his hands), and now and then he gets
// down and goes to one of his spots and back. Look at him, or talk to him: his "..." is over his head, as anyone's words
// are, and Dad says what he means. Asked along, he joins: Dad and he are a team of two (g.team), switched between by the
// portraits or the keys 1 and 2. As him, the cooler on the far sand is a thing to nibble (figure.play("nibble")). Dad has a
// pack of gum and his sunglasses to hand over (by the portrait, or by a click on him): the gum goes in the stash, and the
// sunglasses go on (figure.variant("shades"), set again from the fact "proof.shades" whenever the scene is built: nothing
// of it is saved). "proof-critter" is a cutscene he is in, to be skipped.
const painted = (g) => !!g.flag("proof.painted");
const party = (g) => !!g.flag("proof.party") || !!g.flag("proof.thought");      // (ENGINE-17: the thoughts' proof has the two of them as a party too)
const joined = (g) => !!g.flag("proof.critterJoined");
const CRITTER_AT = [520, 470];                                                  // where he sits up, one of the scene's people
const CRITTER = {
  id: "proof.critter",
  start: (g) => (g.flag("proof.critterMet") ? "ask" : "hello"),
  nodes: {
    hello: { say: ["proof.critter.dots", "proof.critter.hello.dad"], then: (g) => { g.flag("proof.critterMet", true); return "ask"; } },
    ask: {
      options: [
        { id: "what", line: "proof.critter.opt.what", say: ["proof.critter.dots", "proof.critter.what.dad"] },
        { id: "join", line: "proof.critter.opt.join", say: ["proof.critter.dots", "proof.critter.join.dad"], do: (g) => join(g), then: "exit" },
        { id: "bye", line: "proof.critter.opt.bye", say: ["proof.critter.dots"], then: "exit" },
      ],
    },
  },
};
/** He comes along: from one of the scene's people to a lead, on a team of two with Dad, where he stands. */
function join(g) {
  const c = g.actor("critter"), d = g.store.data;
  if (!c) return;
  d.where.critter = { scene: g.scene.id, x: Math.round(c.x), y: Math.round(c.y), face: c.yaw };
  g.flag("proof.critterJoined", true);
  g.team(["dad", "critter"]);
}
/** As him, at the cooler: a good long nibble at the lid (figure.play, for so long), and what Dad makes of it. */
async function nibble(g) {
  await g.lead.play(g.clock, "nibble", { ms: 1800 });
  await g.say("proof.critter.dots");
  if (g.actor("dad")) await g.say("proof.critter.nibble.dad");
  g.flag("proof.nibbled", true);
}
/** A cutscene he is in (g.cutscene("proof-critter")): he scampers to the cooler (hurried, he runs), has a go at it, and
    Dad has his say. Skipped, it ends with him at the cooler and everything said counted. */
async function critterRun(g) {
  const c = g.actor("critter");
  if (!c) return;
  c.hurry = true;
  await g.walkTo(690, 380, "critter");
  await c.play(g.clock, "nibble", { ms: 1500 });
  await g.say("proof.critter.dots", "proof.critter.nibble.dad");
  g.flag("proof.scampered", true);
}
/** Something handed to him: into the stash, and a word about it; the sunglasses go on. */
async function given(g, item, to) {
  if (to !== "critter") return;
  await g.say("proof.critter.dots");
  if (item !== "sunglasses") return g.say("proof.critter.given.dad");
  const stash = g.store.data.inventory.critter;
  stash.splice(stash.indexOf("sunglasses"), 1);                                // (he wears them)
  g.flag("proof.shades", true);
  const c = g.actor("critter");
  if (c && c.variant) c.variant("shades");
  await g.say("proof.critter.shades.dad");
}
// The party of two (NEVADA-12E): while "proof.party" is true (index.html?scene=engine-proof&lead=dad&flags=proof.party) Dad
// and the creature are here together, as Mom and the girls are in the house: a mark each when the scene opens with them,
// and a way in (`fromTrack`) by which they arrive together. They talk (`talk`), hand things over (`given`), and each has a
// hint for the proof's one beat, whose lead is the two of them (PROOF_ACT): his is "..." and what Dad says it means.
const PROOF_ACT = { id: "proof", title: "The engine's proof", era: "egypt", summary: "Not part of the story: the proof scene's own beat, for its tests.",
  beats: [
    { id: "proof.together", kind: "cutscene", title: "Dad and the creature, a party of two", lead: ["dad", "critter"], scene: "engine-proof", needs: [], sets: "proof.party" },
    { id: "proof.cooler", kind: "puzzle", chain: "A", title: "Get into the cooler: a job for small hands", lead: ["dad", "critter"], scene: "engine-proof",
      needs: ["proof.party"], sets: "proof.nibbled", hint: { dad: "proof.hint.party.dad", critter: ["proof.critter.dots", "proof.hint.party.critter.dad"] } },
  ] };
// ENGINE-17: the thoughts' proof (proof.thought) has a beat of its own, open from the start, in an act of its own that is put in
// the story only then (setup), so that no other proof's story check ever meets it: the critter's hint is a thought, and then
// what Dad makes of it.
const THOUGHT_ACT = { id: "proof-thought", title: "The engine's proof: thoughts", era: "egypt", summary: "Not part of the story: the thoughts' proof's own beat, for its tests.",
  beats: [{ id: "proof.thinking", kind: "puzzle", chain: "B", title: "A hint that is a thought", lead: ["dad", "critter"], scene: "engine-proof", needs: [], sets: "proof.thought.done",
    hint: { critter: ["proof.critter.think.hint", "proof.hint.thought.dad"], dad: "proof.hint.thought.dad2" } }] };
/** What the story needs for the creature while he is here: the proof's beat, his stock replies ("..."), and what he and Dad say on looking at each other. */
function critterStory(g) {
  const st = g.story;
  if (!st.acts.some((a) => a.id === PROOF_ACT.id)) st.acts.push(PROOF_ACT);
  for (const kind of ["nope", "look", "hint"]) if (st.fallbacks[kind] && !st.fallbacks[kind].critter) st.fallbacks[kind].critter = ["proof.critter.dots"];
  st.see = st.see || {};
  st.see.dad = { ...(st.see.dad || {}), critter: "proof.critter.look" };
  st.see.critter = { ...(st.see.critter || {}), dad: "proof.critter.dots" };
  if (!g.cutscenes["proof-critter"]) g.cutscenes["proof-critter"] = critterRun;
}

// ---------- NEVADA-12E: a strip of painting going by behind a window (docs/DESIGN.md, section 2, "Things that move by nature") ----------
// On the stage while "proof.strip" is true: index.html?scene=engine-proof&lead=dad&flags=proof.strip. A panel of the engine's
// own stands on the far sand (art/proof/window.png, a cut-out with two holes in it), and a strip of desert painted to run on
// from its right edge into its left (art/proof/strip.png, 480 x 80) goes by behind the holes, to the left, as from a car.
const strip = (g) => !!g.flag("proof.strip");
const PANES = [[[452, 318], [531, 318], [531, 363], [452, 363]], [[550, 318], [629, 318], [629, 363], [550, 363]]];     // the holes, pixel for pixel

// ---------- ROME-13E: round thirteen's three proofs: a flock herded into a pen, a boat riding the water, a man at a window ----------
// The lines are the proof's own, added to the game's as the scene is built (setup), as the others are.
const LINES13 = {
  "proof.geese.look": ["dad", "Six white geese with orange bills, standing about on the sand as if they owned it. They might."],
  "proof.geese.stomp": ["dad", "HUP! Go on, the lot of you! Into the pen!"],
  "proof.geese.herded": ["dad", "And in they go. Let the record show that I never touched a single goose."],
  "proof.geese.penned": ["dad", "Six geese in a pen, looking at me as if it was their idea."],
  "proof.pen.look": ["dad", "A little pen of posts and rails, with a gap in the front for geese. Built by an optimist."],
  "proof.pen.use": ["dad", "In you go, geese. Into the nice pen. Please?"],
  "proof.geese.hiss": ["dad", "They hissed at me. All six of them. In harmony."],
  "proof.pen.full": ["dad", "They're in. I'm not going in there after them."],
  "proof.boat.look": ["dad", "A little rowing boat, tied up at the bank. It isn't going anywhere. It just goes up and down."],
  "proof.house.look": ["dad", "A plain plastered house. One door, one window, and somebody at the window."],
  "proof.housedoor.look": ["dad", "His front door, standing open. Polite people knock anyway."],
  "proof.housedoor.knock": ["dad", "Knock, knock."],
  "proof.watcher.look": ["dad", "A man at his upper window, praying. He knows I'm here. He's finishing first."],
  "proof.watcher.hello.dad": ["dad", "Hello up there!"],
  "proof.watcher.hello": ["watcher", "Peace to you, friend. I am at my prayers. Knock, and I will come down."],
  "proof.watcher.coming": ["watcher", "I am coming."],
  "proof.watcher.down": ["watcher", "Here I am, friend. My stairs get steeper every year."],
  "proof.watcher.look.down": ["dad", "The man from the window, down here with the rest of us."],
  "proof.watcher.down.2": ["watcher", "A fine morning for standing about. You do it well."],
};

// The geese (docs/DESIGN.md, section 2, "Things that move by nature": the flock, herded). On the stage while "proof.herd" is
// true: index.html?scene=engine-proof&lead=dad&flags=proof.herd. Six white geese of the engine's own (art/proof/goose-*.png,
// painted frames: every set the Capitol's geese have, `run` and `flap` among them, drawn by tools/proof13.py beside the game)
// stand about round a spot on the sand. A little pen of posts and rails stands further up it: its front fence, with a gap
// in it, is a cut-out whose base is that front (art/proof/pen.png); its back fence is behind everybody (pen-back.png), as a
// backdrop would have it. Shoo the geese and Dad stomps: they flap and run, the nearest to him first, through the gap into
// the pen (g.effects.get("geese").herd(...)), and the fact "proof.herded" is set. The scene's `fx` is a function of the game
// (below), which gives the flock the pen for its area from that fact: entered again, they are in it at once. Asked nicely
// into the pen (the pen: Use), every goose stretches its neck out and hisses (pose("look", 1.2)).
const herdProof = (g) => !!g.flag("proof.herd");
const herded = (g) => !!g.flag("proof.herded");
const GOOSE = { dir: "art/proof/", foot: [46, 68], face: "E", sizeAt: 590,
  stand: ["goose-stand-0.png", "goose-stand-1.png"], look: ["goose-look-0.png", "goose-look-1.png"], walk: [0, 1, 2, 3].map((i) => `goose-walk-${i}.png`),
  run: [0, 1, 2, 3].map((i) => `goose-run-${i}.png`), turn: ["goose-turn-0.png"], peck: ["goose-peck-0.png", "goose-peck-1.png"], flap: ["goose-flap-0.png", "goose-flap-1.png"] };
const GEESE_AT = [[262, 482], [400, 478], [426, 504], [396, 532], [282, 534], [250, 508]];       // their spot on the sand
const PEN_IN = [[452, 409], [550, 409], [554, 437], [448, 437]];                                  // inside the pen: their area once they are herded
const PEN_GAP = [501, 447];                                                                        // the gap in its front fence (its middle, on its front row)
/** Dad stomps (two stamps of the foot), and the geese run for the pen, through its gap, the nearest to him first. */
async function stomp(g) {
  const geese = g.effects.get("geese"), me = g.lead, y0 = me.y;
  await g.say("proof.geese.stomp");
  for (let i = 0; i < 2; i++) await g.tween(150, (k) => me.place(me.x, y0 - 5 * Math.sin(Math.PI * k)));
  if (geese) await geese.herd(PEN_IN, { from: [me.x, me.y], via: PEN_GAP });
  g.flag("proof.herded", true);
  await g.say("proof.geese.herded");
}
/** Asked nicely into the pen, every goose stretches its neck out and hisses, for a moment. */
async function shoo(g) {
  const geese = g.effects.get("geese");
  await g.say("proof.pen.use");
  const hiss = geese ? geese.pose("look", 1.2) : null;
  await g.say("proof.geese.hiss");
  await hiss;
}

// The boat (docs/DESIGN.md, section 2: `bob`). On the stage while "proof.bob" is true: index.html?scene=engine-proof&lead=dad&
// flags=proof.bob. A little rowing boat of the engine's own (art/proof/boat.png, a cut-out, its base its waterline) lies on
// the river by the bank, rising and falling on the swell and rocking a little (`bob`, among the moving things below). The
// papyrus in the corner is cleared away while it is there (a script's show(false) on that cut-out: setup), or it would hide it.
const bobProof = (g) => !!g.flag("proof.bob");

// The man at the window (docs/DESIGN.md, section 3, "Someone above the floor"). On the stage while "proof.window" is true:
// index.html?scene=engine-proof&lead=dad&flags=proof.window. A plastered house front of the engine's own stands on the sand
// (art/proof/wall.png, a cut-out, its base its foot, its upper window's opening cut clear; art/proof/room.png, the dark room
// seen through the window, behind everybody, as a backdrop would have it), and a man (`watcher`, the date seller's figure)
// stands at the upper window, praying: one of the scene's people whose feet are on the floor of the upper room, above the
// wall's base and so behind it, drawn at a `scale` of his own (a man a step back from the window: the sill at his waist),
// `solid: false`, his life still, his area the opening. Knock at his door and he comes down: he turns from the window and
// is gone, and steps out of his doorway onto the sand under the same id, at the size of that row, and goes to a spot of his.
// The fact "proof.windowDown" says where he is whenever the scene is built: two entries under `actors` with the same id and
// opposite `when`s, and two areas likewise.
const windowProof = (g) => !!g.flag("proof.window");
const down = (g) => !!g.flag("proof.windowDown");
const UPSTAIRS = [373, 307];               // under his feet, on the floor of the upper room, a step back from the window
const UPSTAIRS_SCALE = 0.5;                // the size of a man standing there (the row's own size, 0.3, would make him tiny)
const OPENING = [[352, 205], [394, 205], [394, 261], [352, 261]];          // the window's opening, pixel for pixel
const HOUSE = [[250, 173], [430, 173], [430, 430], [250, 430]];            // the house front
const DOORWAY = [[270, 331], [310, 331], [310, 430], [270, 430]];          // its door
const OUT_DOOR = [290, 440];               // where he steps out of it, onto the sand
const DOWNSTAIRS = [236, 492];             // and where he goes to stand
/** At the window: a word up to him, and his answer over his head. His prayer goes on. */
const hello = (g) => g.say("proof.watcher.hello.dad", "proof.watcher.hello");
/** A knock at his door: he finishes, turns from the window and goes in, and comes out of his door onto the sand. */
async function comeDown(g) {
  await g.say("proof.housedoor.knock", "proof.watcher.coming");
  const w = g.actor("watcher");
  if (!w) return;
  w.pray(false);
  await g.wait(320);
  w.face("N");
  await g.tween(300, (k) => w.fade(1 - k));                                         // back from the window, and out of sight
  await g.wait(700);                                                                 // (down the stairs inside)
  w.place(OUT_DOOR[0], OUT_DOOR[1], scaleAt(g.scene, OUT_DOOR[1])).face("S");       // out of his door, at the size of that row
  w.fade(1);
  g.flag("proof.windowDown", true);
  await g.walkTo(DOWNSTAIRS[0], DOWNSTAIRS[1], "watcher");
  w.face("E");
  await g.say("proof.watcher.down");
}

// ---------- DRIVE-16E: the world going by a car's side windows (docs/DESIGN.md, section 2, "The world going by a car's side windows") ----------
// On the stage while "proof.drive" is true: index.html?scene=engine-proof&lead=dad&flags=proof.drive. A car's side of the engine's
// own, seen from the back seat (art/proof/drive/car.png, a cut-out behind everybody: a grey band with a window cut clear each
// side of the vanishing point, a small cross on the vanishing point between them), and through the windows the world goes by
// as from a car driving into the picture (`drive`, among the moving things below), drawn by the engine from the proof's own
// camera (DRIVE_CAM) and pictures (art/proof/drive/, painted by tools/paint/proof_drive.py: squares and stripes for the ground,
// plain triangles for the ranges, posts, poles and a marker of plain colours). The stripes along the road run to the cross;
// a post comes out of the far end of a window small and slow and goes out at its near edge large and fast; the far triangles
// hardly move and the near ones drift; the two sides are different places. `g.effects.get("drive-l").set({ speed: 0 })` parks it.
// DRIVE-16F: and each thing's shadow lies on the ground, laid by the engine from `sun` (the limousine's morning: a metre of
// height throws its shadow 0.36 m ahead and 1.95 m to the car's left: out across the ground on the left, in toward the road
// on the right).
const driveProof = (g) => !!g.flag("proof.drive");
const DRIVE_CAM = { vanish: [400, 226], focal: 320, eye: 1.6 };            // level; the eye 1.6 m above the road
const DRIVE_PANES = {                                                      // the windows, their tops and bottoms running to the vanishing point
  L: [[[40, 120], [300, 196.56], [300, 254.89], [40, 330]]],
  R: [[[760, 120], [500, 196.56], [500, 254.89], [760, 330]]],
};
const DRIVE_ART = "art/proof/drive/";
/** One side of the proof's road: its own ground, ranges and things. */
const proofDrive = (side) => ({ id: `drive-${side.toLowerCase()}`, type: "drive", side, windows: DRIVE_PANES[side], ...DRIVE_CAM, speed: 12,
  sky: DRIVE_ART + "sky.png",
  bands: [{ src: `${DRIVE_ART}far-${side.toLowerCase()}.png`, distance: 3000, ppm: 0.1 }, { src: `${DRIVE_ART}mid-${side.toLowerCase()}.png`, distance: 400, ppm: 0.5 }],
  ground: { src: `${DRIVE_ART}ground-${side.toLowerCase()}.png`, from: 4, ppm: 16 },
  things: { src: DRIVE_ART + "things.png", rows: side === "L"
    ? [{ sprite: "pole", every: 45, at: 26, wires: [7.7, 7.4] }, { sprite: "post", every: 5, at: 8, wires: [1.0, 0.6] }, { sprite: ["bush", "cone"], every: [6, 24], at: [9, 40] }]
    : [{ sprite: "marker", every: 30, at: 10 }, { sprite: "board", every: 90, at: 7 }, { sprite: "bush", every: [5, 18], at: [12, 50] }] },
  haze: "#dfe7f0", haze_far: 3000, seed: side === "L" ? 16 : 61, when: driveProof,
  sun: [0.36, 1.95] });                                                    // DRIVE-16F: the things' shadows on the ground (the limousine's sun)

// ---------- ROAD-18E: the drive seen straight ahead (docs/DESIGN.md, section 2, "Straight ahead") ----------
// On the stage while "proof.road" is true: index.html?scene=engine-proof&lead=dad&flags=proof.road,proof.arrived. The stage is
// given over to a drive straight down a road (`side: "ahead"`), from the highway's camera (ROAD_CAM: the vanishing point
// (400, 330), focal 800, the eye 2.70 m up) and the engine's own plain pictures (art/proof/road/, painted by
// tools/paint/proof_road.py): a sky; the road from above in squares, with its yellow centre line in dashes, its white edge
// lines and red bands across its shoulders; the desert either side in squares, with stripes along the road 10 m and 20 m out
// (they run to the vanishing point); brown poles 7.5 m left with their wires, white posts either side, bushes and stones on
// both sides, each on its shadow toward us (the sun dead ahead); and the sign (a green board, B 40) standing 5.95 m right of
// the middle of the road, 317.3 m along it (`pieces`: so that with the camera 300 m along it is 17.3 m ahead, and drawn pixel
// for pixel as the painting's sign is: its board on x 599 to 752), the rows of things kept off the road round it (`gap`). The
// proof's car stands still in the lane (a cut-out at row 548) while the road goes by under it; the hole in time is open on
// the vanishing point (`road-hole`, its paint read again each time the drive draws: the far road bends as it goes by), and
// the hole's glow runs down the road (a light of the drive's). The sign's own rings (`road-sign`, shut) read the drive and,
// as much as the alpha of their second `under` says, the sign as it will be (`sign-bc`). The palms, the papyrus, the wagon
// and the lead are cleared away while it is there (setup). `g.effects.get("road").set({ s: 300 })` puts the camera where the
// sign is 17.3 m ahead, parked; `.set({ speed: 20 })` drives on.
const roadProof = (g) => !!g.flag("proof.road");
const ROAD_CAM = { vanish: [400, 330], focal: 800, eye: 2.7 };
const ROAD_ART = "art/proof/road/";
const ROAD_SIGN = { X: 5.95, s: 317.3 };                                   // the sign's foot: across the road, and along it
const proofRoad = () => [
  { id: "road", type: "drive", side: "ahead", ...ROAD_CAM, speed: 20, sky: ROAD_ART + "sky.png",
    grounds: [{ src: ROAD_ART + "desert-l.png", from: -30, to: -6, ppm: 16 }, { src: ROAD_ART + "road.png", from: -6, to: 6, ppm: 32 }, { src: ROAD_ART + "desert-r.png", from: 6, to: 30, ppm: 16 }],
    things: { src: ROAD_ART + "things.png", rows: [
      { sprite: "pole", every: 40, at: -7.5, wires: [8.1, 7.6], offset: 18, gap: false },      // (the poles go on through the gap, wires and all)
      { sprite: "post", every: 30, at: [-3.6, 3.6], offset: 12 },                               // a post either side of the road
      { sprite: ["bush", "bush-2", "bush", "stone"], every: [3, 12], at: [6.5, 40], both: true } ] },      // either side, at random
    pieces: [{ id: "sign", sprite: "sign", ...ROAD_SIGN }],
    gap: [[ROAD_SIGN.s - 14, ROAD_SIGN.s + 10]],
    sun: [-5.5, 0], shade: "#4a3a6a", shade_k: 0.5, haze: "#f2d2a0", haze_far: 1200, far: 2000,
    light: [{ id: "glow", poly: [[398, 331], [402, 331], [710, 600], [90, 600]], radial: { at: [400, 331], r: [527, 228.65] }, stops: [[0, "#7ff5ff", 0.45], [1, "#7ff5ff", 0]] }],
    seed: 18 },
  { id: "road-hole", type: "portal", at: [400, 330], r: 40, rise: true, open: 1, base: 331, pale: "#fff2c8", under: [{ fx: "road" }] },
  { id: "road-sign", type: "portal", at: [675, 332], r: 44, wide: 2.4, keep: [599, 752], base: 332, pale: "#fff2c8", strength: 0.8,
    under: [{ fx: "road" }, { fx: "road", piece: "sign", sprite: "sign-bc", alpha: 0 }] },     // (the second: what the rings bring through, and how much of it)
];

// ---------- ENGINE-17: round seventeen's proofs: thoughts, a grille, a thing handed across, two floors, the speakers ----------
// What the Office (Act Five, stage one) needs of the engine, each on the stage while its fact is true (add ",proof.arrived"):
//   index.html?scene=engine-proof&lead=dad&flags=proof.thought       thought pictures (docs/DESIGN.md, section 7, "Thought pictures")
//   index.html?scene=engine-proof&lead=dad&flags=proof.grille        a grate in the sand over a room (section 8, "Looking down through a grille")
//   index.html?scene=engine-proof&lead=dad&flags=proof.pass          Dad up here, the critter down there, a thing handed between them
//                                                                    (section 8, "Two leads in two scenes of one time"; and the map's travel for each)
//   index.html?scene=engine-proof&lead=critter&flags=proof.floors    the wagon's roof, a floor of its own (section 3, "Several floors")
//   index.html?scene=engine-proof&lead=dad&flags=proof.pa            the sand in a building with speakers (section 7, "The building's speakers")
// The room under the sand is js/content/scenes/proof-below.js. The lines are the proof's own, added to the game's as the scene
// is built (setup), as the others are. A line of the critter's that carries pictures (its third element) is said as a
// thought: a bubble over his head (js/art/thoughts.js).
const LINES17 = {
  // proof.thought (index.html?scene=engine-proof&lead=dad&flags=proof.thought): Dad and the critter a party of two again
  "proof.critter.think.pie": ["critter", "...", "pie"],
  "proof.critter.think.pie.dad": ["dad", "He says he's thinking about pie. He's always thinking about pie."],
  "proof.critter.think.three": ["critter", "...", ["piepan", "plus", "banjo"]],
  "proof.critter.think.hint": ["critter", "...", ["switch", "arrow", "fan"]],
  "proof.hint.thought.dad": ["dad", "He says: pull the switch, and the fan stops. I don't know which switch. He's very sure."],
  "proof.hint.thought.dad2": ["dad", "Ask the little one. He thinks in pictures, and the pictures are usually right."],
  "proof.dozer.look": ["dad", "A man asleep sitting up, his tablet on his knees. Dreaming in bubbles, by the look of it."],
  "proof.dozer.wake": ["dozer", "Regulation twenty-two... I am resting my eyes..."],
  "proof.napper.look": ["dad", "Another one, out cold in the sand. It must be very restful here."],
  "proof.thought.far": ["dad", "Somewhere a long way off, somebody is thinking about a door."],
  "proof.sky.look": ["dad", "Sky. Very blue. Nobody's thinking anything up there."],
  // proof.grille and proof.pass: the grate in the sand, onto the room under it (proof-below.js)
  "proof.grate.look": ["dad", "A grate in the sand. There's a room down there. Somebody's built a basement under the Nile."],
  "proof.grate.nodrop": ["dad", "Not now. Somebody's looking right up at the grate."],
  // proof.floors (index.html?scene=engine-proof&lead=critter&flags=proof.floors): the wagon's roof, a floor of its own
  "proof.floors.up": ["dad", "That's up on the wagon's roof. I'd have to climb it, and I'm not climbing my own car."],
  "proof.floors.up.critter": ["critter", "...", ["up", "question"]],
  "proof.floors.down": ["dad", "Down there. I'd have to climb down first."],
  "proof.floors.down.critter": ["critter", "...", ["down", "question"]],
  "proof.bumper.look": ["dad", "The back of the wagon. There's a bumper to stand on, and the roof rack above it."],
  "proof.roofedge.look": ["dad", "The edge of the roof. It's a long way down for somebody small."],
  // proof.pa (index.html?scene=engine-proof&lead=dad&flags=proof.pa): the proof's building has speakers
  "proof.pa.pole.look": ["dad", "A loudspeaker on a pole, in the middle of the desert. Somebody likes announcements."],
  "proof.pa.ask": ["dad", "Hello? Is this thing on?"],
  "proof.pa.1": ["houston", "Attention, please. Will the owner of a red station wagon please move it off the river."],
  "proof.pa.2": ["houston", "The pyramid will close at sunset. Please make your way to the exits."],
  "proof.pa.3": ["houston", "Lost: one water-skin. Answers to nothing. Please see the water carrier."],
};
const thoughtProof = (g) => !!g.flag("proof.thought");
const grilleProof = (g) => !!g.flag("proof.grille") || !!g.flag("proof.pass");
const passProof = (g) => !!g.flag("proof.pass");
const floorsProof = (g) => !!g.flag("proof.floors");
const paProof = (g) => !!g.flag("proof.pa");
// The grate (proof.grille, proof.pass): drawn live on the sand at the front, an area of it a grille onto the room under the
// sand. Dad stands on it (its mark `grate`) and looks down through it; the critter, if it were him, would lie down at it.
const GRATE = [[232, 546], [292, 546], [300, 563], [224, 563]];
const GRATE_AT = [262, 556];
// The wagon's roof (proof.floors): a floor of its own, on top of the luggage, at the wagon's size (it is as far off as the
// wagon is) and in depth just in front of the wagon (its base); the sand has a notch cut where the roof lies over it in the
// picture, since two floors never share a pixel. The critter climbs up by the back of the wagon (g.climbTo, on his `climb`
// frames: he has none, so his walk stands in, and the console says so once), and down the same way.
const SAND = [[352, 300], [640, 300], [780, 326], [780, 596], [60, 596], [150, 470], [240, 384], [312, 322]];
const SAND_NOTCHED = [[352, 300], [640, 300], [780, 326], [780, 388], [640, 388], [640, 422], [780, 422], [780, 596], [60, 596], [150, 470], [240, 384], [312, 322]];
const ROOF = [[652, 398], [748, 398], [748, 410], [652, 410]];
const UP_THE_BACK = [[772, 560], [772, 420]];
/** A thought from somebody who is not on the stage (the Son, centuries off): placed as words are for someone off the stage. */
async function farThought(g) {
  await g.say("proof.thought.far");
  await g.think("son", "hole");
}
/** The man asleep: woken (his thought stops), a word in his sleep, and off again (it comes back). */
async function wake(g) {
  g.think("dozer", null);
  await g.say("proof.dozer.wake");
  g.think("dozer", "zzz", { loop: true });
}

/** Whatever waits in the tunnel for whoever is here comes out of the door, one thing at a time: the pop, a word, and into the pockets. */
async function postArrives(g) {
  for (const entry of g.waiting()) {
    if (g.lead) g.lead.look(DOOR[0], DOOR[1]);
    g.sfx("portal");
    await g.arrive(entry.item, DOOR);
    await g.say(mine(g, "proof.door.came", "proof.door.came.son"));
    g.receive(entry.item);
  }
}

/** A thing goes into the door, for the one at the other end. */
async function putIn(g, item) {
  await g.say(mine(g, "proof.door.put", "proof.door.put.son"));
  await g.reach();
  if (!g.send(item, { to: OTHER[g.store.data.active] })) return;             // (not in these pockets after all: the engine has said so in the console)
  g.sfx("portal");
  const door = g.effects.get("door");
  if (door) await g.tween(500, (k) => door.open(1, { scale: 1 + 0.5 * Math.sin(Math.PI * k) }));      // the door winks as it goes in
  await g.say(mine(g, "proof.door.gone", "proof.door.gone.son"));
}

/** A word through the door with whoever is at the other end. Anything waiting comes out first. */
async function talkThrough(g) {
  if (g.waiting().length) return postArrives(g);
  if (g.store.data.active === "son") { await g.say("proof.door.hello.son"); return g.through("dad", "proof.door.answer.dad"); }
  await g.say("proof.door.hello");
  await g.through("son", "proof.door.answer.1", "proof.door.answer.2");
  for (;;) {
    const pick = await g.choose([{ id: "fine", line: "proof.door.son.fine" }, { id: "send", line: "proof.door.son.send" }, { id: "bye", line: "proof.door.son.bye" }], { through: "son" });
    await g.through("son", `proof.door.son.${pick}`);
    await g.say(`proof.door.${pick}`);
    if (pick === "bye") return;
  }
}

export default {
  id: "engine-proof",
  era: "egypt",
  name: "Where the wagon came down",

  // DEPTH. `horizon` is the row of the picture the ground runs back to, and `full` the row where a person
  // is drawn full size (an adult is 160 pixels tall there). In between, size falls in a straight line:
  //     size = (feet - horizon) / (full - horizon)
  // The painter works from the same two numbers, so doors and wagons come out the right size for the people.
  // minScale stops anyone shrinking to a dot at the far end of the sand.
  horizon: 262, full: 590, minScale: 0.3,

  // WHERE PEOPLE CAN STAND: the sand. The left edge keeps to the bank, clear of the water and of the palms' feet;
  // the far edge stops under the village and the dunes; the right edge keeps a body's width inside the picture.
  // ENGINE-17: a walk can be a function of the game, and can have several floors: while "proof.floors" is true the wagon's
  // roof is a second floor (see the top), joined to the sand only by a climb (g.climbTo). Each floor's `away` is what is
  // said when the player asks for something on the other one.
  walk: (g) => (g && floorsProof(g)                                         // (with no game, as a tool reads it: the sand alone)
    ? { areas: [{ name: "sand", area: SAND_NOTCHED, away: { critter: "proof.floors.down.critter", any: "proof.floors.down" } },
        { name: "roof", area: ROOF, scale: 0.84, base: 546, away: { critter: "proof.floors.up.critter", any: "proof.floors.up" } }] }
    : { area: SAND }),
  spawn: { default: [420, 572], critter: [478, 566], fromTrack: [496, 330],   // (NEVADA-12E: the creature's own mark, and a way in from the track, for the party below)
    grate: GRATE_AT, roof: [700, 404], wagonFoot: [758, 574] },               // (ENGINE-17: on the grate; on the wagon's roof; at the back of the wagon)
  // ENGINE-17: while "proof.pa" is true the sand is in the proof's building (as the room under it always is: proof-below.js), so
  // that a line on its speakers is heard here (g.pa), and now and then the building says something by itself (`announce`).
  building: (g) => (paProof(g) ? "proof" : null),
  announce: { lines: ["proof.pa.2", "proof.pa.3"], every: [25, 40], when: paProof },
  // NEVADA-12E: a party of two who are not family, while "proof.party" is true (see the top): Dad and the creature. A party
  // can be a function of the game, for one the story forms. By the way in from the track the creature arrives beside Dad.
  party: (g) => (party(g) ? ["dad", "critter"] : null),
  arrive: { fromTrack: [[540, 344]] },
  // CAR-13E: the scene seen through the lead's own eyes, while "proof.unseen" is true (index.html?scene=engine-proof&lead=dad&
  // flags=proof.unseen), as the inside of the wagon is: Dad is on the stage and never drawn (nor is anyone of the team here);
  // a click on the sand moves nobody; the river, the reeds and the wagon are looked at and used from where he stands, without
  // his walking or turning; his words are written off the stage, at the top middle; and a click in the band of a way out
  // takes him out at once (docs/DESIGN.md, section 8, "A scene seen through the lead's own eyes"). Read as the scene is entered.
  unseen: (g) => !!g.flag("proof.unseen"),
  //   wordsAt: [400, 120],          (CAR-13E) where the words of anyone off the stage go, in place of the top middle (the engine's test gives it one)

  picture: art + "back.png",

  // CUT-OUTS. Where each one sorts among the people is its `base`:
  //   a number          the row where it meets the ground. Feet above that row are behind it, feet below in front.
  //   [[x, y], [x, y]]  a line, for a thing that meets the ground on a slant
  //   plane: "front"    in front of everybody, always ("back": behind everybody)
  // `solid` is the patch of ground a cut-out takes up. Nobody can stand in it, and routes go round it.
  planes: [
    // Three palms in a row that runs away from us along the bank: their feet are at (187, 407), (250, 357) and (298, 321),
    // so the base is the line through them. (One row for all three would put people behind a trunk whose foot is behind them.)
    { id: "palms", src: art + "palms.png", base: [[187, 407], [298, 321]] },
    { id: "wagon", src: art + "wagon.png", base: [[490, 541], [790, 537]],        // along the wheels, nose to tail
      solid: [[470, 528], [790, 522], [796, 548], [470, 556]] },                  // the ground under the car (the sand heaped at its nose can be walked behind)
    { id: "papyrus", src: art + "front.png", plane: "front" },                    // the papyrus at the bottom left corner
    // NEVADA-12E: the panel with two windows in it, for the strip (see the top); there only while "proof.strip" is true
    { id: "window", src: "art/proof/window.png", base: 372, solid: [[440, 364], [640, 364], [640, 374], [440, 374]], when: strip },
    // ROME-13E: the geese's pen (see the top): its back fence behind everybody; its front, with the gap, a cut-out on its front row
    { id: "pen-back", src: "art/proof/pen-back.png", plane: "back", when: herdProof },
    { id: "pen", src: "art/proof/pen.png", base: 446, solid: [[436, 400], [566, 400], [566, 448], [436, 448]], when: herdProof },
    // ROME-13E: the boat on the river (see the top), its base its waterline: it bobs (`fx`, below)
    { id: "boat", src: "art/proof/boat.png", base: 456, when: bobProof },
    // ROME-13E: the house front (see the top): the dark room behind its window, behind everybody; the wall, its base its foot
    { id: "room", src: "art/proof/room.png", plane: "back", when: windowProof },
    { id: "wall", src: "art/proof/wall.png", base: 430, solid: [[250, 400], [430, 400], [430, 432], [250, 432]], when: windowProof },
    // DRIVE-16E: the car's side, seen from the back seat, with a window each side of the vanishing point (see the top)
    { id: "car", src: DRIVE_ART + "car.png", plane: "back", when: driveProof },
    // ROAD-18E: the proof's car, standing still in the lane at row 548 while the road goes by under it (see the top)
    { id: "road-car", src: ROAD_ART + "car.png", at: [521, 548], foot: [73.5, 121], base: 548, when: roadProof },
  ],
  // A cut-out can also follow the story. These are the other forms (none is needed here):
  //   { id: "trunk", src: art + "trunk-open.png", base: 541, when: (g) => g.flag("egypt.trunkOpen") }      a row for a base; shown only while the test passes
  //   { id: "screen", base: 380, state: (g) => (g.flag("home.online") ? "login" : "offline"),              one of several pictures
  //     states: { offline: "art/scenes/home/screen-offline.png", login: "art/scenes/home/screen-login.png" } },
  //   { id: "steam", frames: [art + "steam-0.png", art + "steam-1.png"], fps: 6, at: [520, 470], foot: [20, 60], plane: "front" }
  //                                                         a small cropped picture, animated: its point `foot` is put at `at`
  // `when` and `state` are read again every time the story changes, so a script only records the fact.
  // A script can also take hold of one: g.plane("trunk").show(true), .set("login"), .fade(0.5), .place(x, y, scale).

  // THINGS THAT MOVE BY NATURE (js/engine/effects.js). Nothing that moves by itself in the world is painted still: the
  // painter leaves it out and marks where it goes (layout.json, "fx"), the scene lists it here, and the engine draws it
  // moving, on the game clock, among the people at its own depth (`base` or `plane`, as for a cut-out). They are on the
  // stage only while the story fact "proof.fx" is true (index.html?scene=engine-proof&lead=dad&flags=proof.fx), so that
  // everything else here is as it was. Every kind, every field and its default: docs/DESIGN.md, "Things that move by nature".
  // ROME-13E: a function of the game, as a scene whose moving things follow the story has it: the geese's area is their spot,
  // or the pen once they have been herded into it (a fact), as the scene is built.
  fx: (g) => [
    // the builders' village, far off: a cooking fire's smoke, a thin pale thread that rises a little and bends away with the air
    { id: "village-smoke", type: "smoke", at: [392, 286], base: 296, color: "#f4ecdc", opacity: 0.38, height: 36, width: [1.5, 10], lean: [34, -34], when: fx },
    // a fire on the sand: a bed of coals, a flame, and a column of smoke a man can walk behind or in front of (base: where it stands)
    { id: "fire-coals", type: "embers", at: [468, 430], size: [9, 3], base: 430, when: fx },
    { id: "fire", type: "flame", at: [468, 429], size: 13, base: 430, when: fx },
    { id: "fire-smoke", type: "smoke", at: [468, 422], base: 430, height: 130, width: [6, 46], rise: 20, wind: 7, opacity: 0.45, when: fx },
    // light moving on the river, kept off the boat and the reeds; now and then a ring where a fish comes up
    { id: "river", type: "shimmer", when: fx,
      poly: [[0, 264], [344, 264], [321, 276], [295, 300], [261, 336], [213, 384], [149, 440], [83, 492], [19, 530], [0, 532]],
      holes: [[84, 280, 98, 62], [280, 287, 22, 24], [249, 308, 24, 33], [214, 335, 27, 41]] },
    { id: "fish", type: "ripples", at: [206, 300], every: [2, 6], radius: 14, when: fx },
    // doves on the bank between the palms: they peck and potter, go up when somebody comes near, and land again further off
    { id: "doves", type: "birds", look: "dove", count: 6, area: [[268, 372], [318, 334], [372, 338], [392, 372], [330, 402], [282, 400]], when: fx },
    // small birds crossing high up now and then, and two kites wheeling over the pyramid
    { id: "swallows", type: "birds", lanes: [[[-20, 46], [820, 22]], [[820, 62], [-20, 80]]], every: [4, 10], group: [1, 3], when: fx },
    { id: "kites", type: "birds", circle: { at: [560, 58], r: [42, 13] }, count: 2, size: [7, 9], when: fx },
    // the palms' crowns and the papyrus stir in the warm wind off the river (their feet do not move)
    { id: "palms-sway", type: "sway", plane: "palms", anchor: "bottom", amount: 1.4, when: fx },
    { id: "papyrus-sway", type: "sway", plane: "papyrus", anchor: "bottom", amount: 1.2, when: fx },
    // water from a spout, splashing where it lands: here, to show it, meltwater pouring off the roof from the cooler
    { id: "spill", type: "stream", path: [[749, 427], [756, 431], [761, 440], [764, 470], [765, 505], [766, 546]], width: [1.5, 2.5], base: 549, when: fx },
    // LETTERBOX-11: the small door in time, open, in the air over the sand (the paint bending, as the chamber's door is): see the top
    { id: "door", type: "portal", at: DOOR, r: 34, base: DOOR[1] + 34, open: 1, strength: 0.6, when: letterbox },
    // NEVADA-12E: the desert going by behind the panel's two windows (see the top), behind everybody
    { id: "desert", type: "strip", src: "art/proof/strip.png", windows: PANES, row: 370, speed: 40, loop: true, plane: "back", when: strip },
    // ROME-13E: the geese (see the top): round their spot, or in the pen once herded; sacred enough not to be shy of anybody
    { id: "geese", type: "birds", count: 6, area: herded(g) ? PEN_IN : GEESE_AT, frames: GOOSE, shy: 0, fly: false, walk: 28, moves: { stand: 3, look: 2, peck: 3, walk: 2, turn: 1 }, when: herdProof },
    // ROME-13E: the boat (see the top) rising and falling a pixel on the swell, and rocking a little
    { id: "boat-bob", type: "bob", plane: "boat", amount: 1, period: 5, tilt: 0.75, when: bobProof },
    // DRIVE-16E: the world going by the car's windows (see the top), one each side of the road, behind everybody
    proofDrive("L"), proofDrive("R"),
    // ROAD-18E: the drive straight ahead, the hole on the vanishing point, the sign's rings (see the top): on the stage only
    // when the scene is built with the fact proof.road (so that the other proofs' lists of moving things are as they were)
    ...(roadProof(g) ? proofRoad() : []),
  ],

  // Light that must stay smooth (a wormhole, a beam, a glow) is not painted. A scene draws it live, in the same pixels:
  //   live(art, g) { return art.portal(500, 300, 40, "door"); },        and a script finds it with g.q("#door")
  // ENGINE-17: and stand-ins for things not painted: the grate in the sand (proof.grille, proof.pass), the loudspeaker on its
  // pole (proof.pa). (The live layer is under the cast: whoever stands on the grate is drawn over it.)
  live(art, g) {
    let out = "";
    if (grilleProof(g)) {
      out += `<g id="grate"><polygon points="${GRATE.map((p) => p.join(",")).join(" ")}" fill="#2e2924" stroke="#1a1612" stroke-width="1.5"/>`;
      for (const y of [549.5, 553.5, 557.5]) out += `<line x1="${230 + (y - 546) * 0.35}" y1="${y}" x2="${294 - (y - 546) * -0.35}" y2="${y}" stroke="#9a948a" stroke-width="2"/>`;
      out += `</g>`;
    }
    if (paProof(g)) out += `<g id="pa-pole"><line x1="598" y1="338" x2="598" y2="288" stroke="#4a3f36" stroke-width="3"/>` +
      `<polygon points="597,290 615,281 615,301" fill="#c9cdd3" stroke="#3a332c" stroke-width="1.2"/><rect x="590" y="287" width="8" height="7" fill="#8e949c" stroke="#3a332c" stroke-width="1"/></g>`;
    return out;
  },

  // WAYS OUT AT THE EDGES OF THE PICTURE. Over the floor near an edge that has one, the pointer becomes an arrow and the
  // label says where it leads ("Go up the track"); a click there walks the lead to that edge, and on (js/engine/edges.js).
  //   N, S, W, E     the top, the bottom, the left and the right of the picture
  //   to, spawn      the scene, and the named way in at the other end, as g.goto(to, { spawn }) takes them
  //   name           what the label says after "Go". With none: "Go to" and the other scene's name.
  //   walkTo         where the lead walks before leaving. With none: the floor nearest the click, as far toward the edge as it goes.
  //   when(g)        the way is there only while this is true (until then its band is plain floor)
  //   use(g)         a script to run instead of the plain g.goto: a way that is also a gate, or that needs a line first
  // A clickable area in a band always wins over it. (This scene has no S edge: the tests click along the front of the sand.)
  edges: {
    N: { to: "sketch-example", name: "up the track", walkTo: [496, 302] },
    E: { to: "sketch-example" },                                                 // the label is "Go to a market street (not painted yet)"
    W: { to: "sketch-example", name: "across the river", when: (g) => !!g.flag("proof.ferry"),
      use: async (g) => { await g.say("egypt.river.look"); await g.goto("sketch-example"); } },
  },

  // CLICKABLE AREAS. Show (or holding H) draws an outline round each, following its poly, rect or circle; so make a shape
  // hug its thing. An area that is a cut-out (`plane: "<plane id>"`, or a plane with the same id, as the wagon here) is
  // outlined by the cut-out's own silhouette instead, as much of it as lies inside the area.
  hotspots: [
    { id: "pyramids", name: "pyramids", rect: [432, 78, 368, 172], look: "egypt.pyramids.look" },
    { id: "river", name: "river", poly: [[0, 262], [345, 262], [20, 530], [0, 545]], walkTo: [200, 440], face: "W", look: "egypt.river.look" },
    { id: "reeds", name: "reeds", poly: [[132, 384], [214, 330], [280, 286], [300, 290], [300, 312], [240, 376], [178, 440], [136, 440]], walkTo: [262, 380], face: "W", look: "egypt.reeds.look" },
    { id: "wagon", name: "wagon", poly: [[462, 492], [560, 470], [600, 420], [650, 388], [750, 394], [790, 440], [790, 520], [740, 544], [462, 520]], walkTo: [600, 574], face: "N", look: "egypt.wagon.look",
      when: (g) => !floorsProof(g) },
    // ENGINE-17: while the wagon's roof is a floor (proof.floors), the wagon's area stops short of it, so that a click there is a
    // click on the roof's floor (to walk along it, or to be told it is another floor)
    { id: "wagon", name: "wagon", poly: [[462, 492], [560, 470], [600, 420], [640, 414], [756, 414], [790, 440], [790, 520], [740, 544], [462, 520]], walkTo: [600, 574], face: "N", look: "egypt.wagon.look",
      when: floorsProof },
    // The two people (below, under `actors`), while "proof.life" is true: each area is the figure at its mark. Away from
    // the mark on a walk of their own, the area goes with them (js/engine/life.js); a click brings them home to talk.
    { id: "scribe", name: "scribe", verb: "Talk to", rect: [550, 339, 32, 37], walkTo: [604, 384], face: "W", when: (g) => !!g.flag("proof.life"),
      look: "egypt.scribe.look", use: ["egypt.scribe.meet.1"] },
    { id: "overseer", name: "overseer", verb: "Talk to", rect: [279, 364, 44, 114], walkTo: [352, 478], face: "W", when: (g) => !!g.flag("proof.life"),
      look: "egypt.overseer.look", use: ["egypt.overseer.meet.1"] },
    // LETTERBOX-11: the small door (see the top): a word through it, or a small thing put in it for the one at the other end.
    // Which things fit is this list's say, with a closure for each, since a `useWith` script is handed only the game.
    { id: "door", name: "small door in time", verb: "Speak through", circle: [DOOR[0], DOOR[1], 42], walkTo: [360, 536], face: "N", when: letterbox,
      look: (g) => g.say(mine(g, "proof.door.look", "proof.door.look.son")), use: talkThrough,
      useWith: Object.fromEntries(SMALL.map((item) => [item, (g) => putIn(g, item)])) },
    // TALK-11: the water carrier (see the top): a talk with him is the tree
    { id: "carrier", name: "water carrier", verb: "Talk to", rect: [232, 381, 36, 100], walkTo: [306, 488], face: "W", when: talk,
      look: "proof.carrier.look", use: (g) => g.talk(CARRIER) },
    // NEVADA-12E: the creature, while he is one of the scene's people (see the top); a companion after he joins, and then
    // the engine gives him the area every companion has
    { id: "critter", name: "small creature", verb: "Talk to", rect: [503, 441, 34, 32], walkTo: [466, 486], face: "E", when: (g) => painted(g) && !joined(g) && !party(g),
      look: "proof.critter.look", use: (g) => g.talk(CRITTER) },
    // NEVADA-12E: the cooler on the far sand, painted in the backdrop: nothing for Dad, a nibble for the creature
    { id: "cooler", name: "cooler", rect: [706, 322, 40, 30], walkTo: [712, 364], face: "N", when: (g) => painted(g) || party(g),
      look: { critter: (g) => g.say(thoughtProof(g) ? "proof.critter.think.three" : "proof.critter.dots"), any: "proof.cooler.look" }, use: { critter: nibble, any: "proof.cooler.use.dad" } },      // (ENGINE-17: thinking, in three pictures)
    // ROME-13E: the geese and their pen (see the top). Shoo the geese: Dad stomps, and they are herded into the pen. The pen,
    // asked of them nicely, makes them hiss. Herded, the geese are clicked in the pen (an area listed after the pen's, so on top)
    { id: "geese", name: "geese", verb: "Shoo", poly: [[240, 428], [440, 426], [444, 540], [240, 542]], walkTo: [290, 568], face: "N", when: (g) => herdProof(g) && !herded(g),
      look: "proof.geese.look", use: stomp },
    { id: "pen", name: "pen", verb: "Use", poly: [[434, 368], [568, 368], [568, 450], [434, 450]], walkTo: [470, 482], face: "N", when: herdProof,
      look: "proof.pen.look", use: (g) => (herded(g) ? g.say("proof.pen.full") : shoo(g)) },
    { id: "geese-penned", name: "geese", poly: [[444, 380], [560, 380], [560, 440], [444, 440]], walkTo: [470, 482], face: "N", when: (g) => herdProof(g) && herded(g),
      look: "proof.geese.penned" },
    // ROME-13E: the boat (see the top): outlined by its own picture, bobbing
    { id: "boat", name: "boat", rect: [32, 432, 100, 26], walkTo: [168, 476], face: "W", when: bobProof, look: "proof.boat.look" },
    // ROME-13E: the house front and the man at its window (see the top). Its door and its window are listed after it: where
    // two areas overlap, the one listed later is on top, and is what a click finds. The man's area is the window's opening
    // (`actor: "watcher"`: Show outlines his own figure inside it); come down, he has an area of his own on the sand.
    { id: "house", name: "house", poly: HOUSE, walkTo: [340, 452], face: "N", when: windowProof, look: "proof.house.look" },
    { id: "housedoor", name: "door", verb: "Knock at", poly: DOORWAY, walkTo: [330, 450], face: "NW", when: (g) => windowProof(g) && !down(g),
      look: "proof.housedoor.look", use: comeDown },
    { id: "atwindow", name: "man at the window", verb: "Talk to", actor: "watcher", poly: OPENING, walkTo: [372, 452], face: "N", when: (g) => windowProof(g) && !down(g),
      look: "proof.watcher.look", use: hello },
    { id: "watcher", name: "man", verb: "Talk to", rect: [212, 378, 48, 116], walkTo: [290, 496], face: "W", when: (g) => windowProof(g) && down(g),
      look: "proof.watcher.look.down", use: ["proof.watcher.hello.dad", "proof.watcher.down.2"] },
    // ENGINE-17: the grate (see the top): a grille onto the room under the sand (proof-below.js). "Look down" is the engine's
    // verb for it; its `spawn` lets whoever looks down drop in, while its `when` allows (proof.noDrop: not now, and its `no`).
    { id: "grate", name: "grate", poly: GRATE, walkTo: GRATE_AT, face: "S", when: grilleProof, look: "proof.grate.look",
      grille: { scene: "proof-below", spawn: "vent", from: [400, 250], when: (g) => !g.flag("proof.noDrop"), no: "proof.grate.nodrop" } },
    // ENGINE-17: the two floors (see the top): up the back of the wagon onto its roof, and down again, by a set path
    { id: "bumper", name: "back of the wagon", verb: "Climb", rect: [748, 448, 42, 72], walkTo: [758, 574], face: "N", when: floorsProof,
      look: "proof.bumper.look", use: (g) => g.climbTo("roof", { path: UP_THE_BACK }) },
    { id: "roofedge", name: "edge of the roof", verb: "Climb down", rect: [736, 390, 24, 24], walkTo: [736, 404], face: "E", when: floorsProof,
      look: "proof.roofedge.look", use: (g) => g.climbTo("wagonFoot", { path: [...UP_THE_BACK].reverse() }) },
    // ENGINE-17: the loudspeaker on its pole (proof.pa): a word into it, and the building answers on its speakers
    { id: "pa-pole", name: "loudspeaker", verb: "Speak to", rect: [586, 278, 32, 62], walkTo: [600, 352], face: "N", when: paProof,
      look: "proof.pa.pole.look", use: async (g) => { await g.say("proof.pa.ask"); await g.pa("proof.pa.1"); } },
    // ENGINE-17: the thoughts (proof.thought): two men asleep, sitting, each thinking zzz (a thought kept up: g.think with
    // loop); and the sky, where the thought of somebody who is not on the stage is put, as his words would be
    { id: "dozer", name: "sleeping man", verb: "Wake", rect: [204, 478, 34, 46], walkTo: [270, 540], face: "W", when: thoughtProof,
      look: "proof.dozer.look", use: wake },
    { id: "napper", name: "man asleep in the sand", rect: [362, 404, 40, 30], walkTo: [400, 470], face: "N", when: thoughtProof, look: "proof.napper.look" },
    { id: "sky", name: "sky", verb: "Wonder about", rect: [60, 20, 300, 110], when: thoughtProof, look: "proof.sky.look", use: farThought },
  ],

  // NEVADA-12E: Dad and the creature, talking (each exchange is what the one clicked on says, then what Dad makes of it)
  talk: {
    dad: { critter: (g) => (thoughtProof(g) ? [["proof.critter.think.pie", "proof.critter.think.pie.dad"]] : [["proof.talk.dad.critter.1", "proof.critter.dots", "proof.talk.dad.critter.1b"]]) },     // (ENGINE-17: a thought, and Dad's reading of it)
    critter: { dad: [["proof.critter.dots", "proof.talk.critter.dad.1"]] },
  },
  given,

  // LETTERBOX-11: what the letterbox proof needs of the story when the scene is built: the two of them a team, the one who is
  // not here placed in another century, and the pack of gum in Dad's pockets, once. (And the proof's lines, for the tests.)
  setup(g) {
    for (const [id, line] of Object.entries(LINES)) if (!g.lines[id]) g.lines[id] = line;
    for (const [id, line] of Object.entries(LINES13)) if (!g.lines[id]) g.lines[id] = line;          // ROME-13E: round thirteen's
    for (const [id, line] of Object.entries(LINES17)) if (!g.lines[id]) g.lines[id] = line;          // ENGINE-17: round seventeen's
    if (thoughtProof(g)) {                                                                            // ENGINE-17: the two asleep, each thinking zzz, kept up
      if (!g.story.acts.some((a) => a.id === THOUGHT_ACT.id)) g.story.acts.push(THOUGHT_ACT);      // (and the thoughts' own beat, for the critter's hint)
      for (const [id, name, color] of [["dozer", "Sleeper", "#ffb48a"], ["napper", "Sleeper", "#c9ced6"]]) if (!g.cast[id]) g.cast[id] = { name, color };
      g.think("dozer", "zzz", { loop: true });
      g.think("napper", "zzz", { loop: true });
    }
    if (passProof(g)) {                                                                               // ENGINE-17: the critter under the sand, Dad up here with the gum
      const d = g.store.data;
      critterStory(g);
      if (!g.flag("proof.passSetup")) { d.where.critter = { scene: "proof-below", x: 560, y: 520, face: 270 }; if (!d.inventory.dad.includes("gum")) d.inventory.dad.push("gum"); g.flag("proof.passSetup", true); }
      if (!d.team.includes("critter")) g.team(["dad", "critter"]);
    }
    if (windowProof(g) && !down(g) && g.actor("watcher")) g.actor("watcher").pray(true);              // ROME-13E: the man at the window, at his prayers
    if (bobProof(g) && g.plane("papyrus")) g.plane("papyrus").show(false);                             // ROME-13E: the papyrus cleared away, so that the boat can be seen
    if (driveProof(g)) for (const id of ["palms", "papyrus"]) if (g.plane(id)) g.plane(id).show(false);    // DRIVE-16E: the palms and the papyrus cleared away, so that the windows can be seen
    if (roadProof(g)) { for (const id of ["palms", "papyrus", "wagon"]) if (g.plane(id)) g.plane(id).show(false); if (g.lead) g.lead.fade(0); }      // ROAD-18E: the stage given over to the road
    // NEVADA-12E: the creature's story, Dad's gum and sunglasses (once), and the creature in his shades if he has them on
    if (painted(g) || party(g)) {
      critterStory(g);
      const d = g.store.data;
      if (!g.flag("proof.critterThings")) { for (const it of ["gum", "sunglasses"]) if (!d.inventory.dad.includes(it)) d.inventory.dad.push(it); g.flag("proof.critterThings", true); }
      const c = g.actor("critter");
      if (c && c.variant) c.variant(g.flag("proof.shades") ? "shades" : null);
    }
    if (!letterbox(g)) return;
    const d = g.store.data;
    for (const id of ["dad", "son"]) if (!d.where[id]) d.where[id] = { scene: "sketch-example", x: 400, y: 560, face: "S" };
    g.team(["dad", "son"]);
    if (!g.flag("proof.gum")) { if (!d.inventory.dad.includes("gum")) d.inventory.dad.push("gum"); g.flag("proof.gum", true); }
  },

  // PEOPLE, AND THEIR OWN LIVES (js/engine/life.js). Two people of the place, on the stage only while the story fact
  // "proof.life" is true (the engine's test turns it on: index.html?scene=engine-proof&lead=dad&flags=proof.life), so
  // that everything else here is as it was. Everyone fidgets now and then by themselves; `life` says what else they do:
  //   the scribe sits on the sand, and now and then gets up, walks up the bank or over toward the wagon, stays a few
  //   seconds, and comes back and sits down again (a seated person can do this once the rig can stand them up);
  //   the overseer stands, and strolls a few steps toward the river or up the sand, and back.
  // A click on someone who is away brings them home first, while the lead walks over; their clickable area goes with them.
  actors: [
    { id: "scribe", kind: "scribe", at: [566, 372], face: "W", when: (g) => !!g.flag("proof.life"),
      life: { every: [14, 26], spots: [[486, 338, "N"], [660, 356, "E"]], stay: [3, 6] } },
    { id: "overseer", kind: "overseer", at: [300, 470], face: "E", when: (g) => !!g.flag("proof.life"),
      life: { every: [16, 30], spots: [[250, 500, "W"], [380, 420, "N"]], stay: [3, 6] } },
    // TALK-11: the water carrier, on the sand by the river while "proof.talk" is true (see the top). No walks of his own: the tree walks him.
    { id: "carrier", kind: "carrier", at: CARRIER_AT, face: "E", when: talk },
    // NEVADA-12E: the painted creature, sitting up (`sit: true`: he is found sitting only when the scene says so), with a
    // life of his own: his small movements are his own sets, and now and then he goes to one of his spots and back
    { id: "critter", kind: "critter", at: CRITTER_AT, face: "W", sit: true, when: (g) => painted(g) && !joined(g) && !party(g),
      life: { every: [12, 22], spots: [[600, 440, "E"], [462, 512, "S"]], stay: [3, 6] } },
    // ROME-13E: the man at the upper window (see the top): his feet on the upper floor behind the wall, a scale of his own, no
    // ground of ours taken up, no small movements while he prays; and the same man on the sand once he has come down
    { id: "watcher", kind: "dateseller", at: UPSTAIRS, scale: UPSTAIRS_SCALE, face: "W", solid: false, life: { fidget: false }, when: (g) => windowProof(g) && !down(g) },
    { id: "watcher", kind: "dateseller", at: DOWNSTAIRS, face: "E", when: (g) => windowProof(g) && down(g) },
    // ENGINE-17: the thoughts' proof: two men asleep sitting up (the rig's seated figures: a scribe cross-legged, and the man in
    // gray in the dust), each with a thought kept over his head (setup), so that a bubble is seen over a seated head
    { id: "dozer", kind: "scribe", at: [220, 520], face: "E", life: { fidget: false }, when: thoughtProof },
    { id: "napper", kind: "agent-collar", at: [382, 432], face: "S", life: { fidget: false }, when: thoughtProof },
  ],

  // Runs when the lead arrives. It must be safe to run twice (a save can be loaded in the middle of it), so it checks its own fact.
  async enter(g) {
    if (!g.flag("proof.arrived")) {
      await g.wait(400);
      await g.say("egypt.arrive.1");
      g.flag("proof.arrived", true);
    }
    if (letterbox(g)) await postArrives(g);          // LETTERBOX-11: anything that came through for whoever has just come in, the door gives up
  },
};

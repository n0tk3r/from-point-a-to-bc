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

const art = "art/scenes/egypt-crash/";
const fx = (g) => !!g.flag("proof.fx");          // the things that move by nature (`fx`, below) are on the stage while this is true

// ---------- LETTERBOX-11: the letterbox, the engine's own proof of it (docs/DESIGN.md, "The letterbox") ----------
// On the stage while "proof.letterbox" is true: index.html?scene=engine-proof&lead=dad&flags=proof.letterbox.
// Dad is here with a pack of gum, and the Son is in another century (the market street sketch, in Rome), so the two are
// a team and switching to him is the short tunnel. A small door in time hangs in the air over the sand. Anything small
// that whoever is here carries can be put in it for the one at the other end (this scene's own choice, SMALL: the engine
// never decides what fits), and it waits in the tunnel, marking that person's portrait, until they take it out of a door
// of theirs. The sketch has no door, so the proof lets the Son take it out of this one: come back here as the Son
// (switch again) and on arrival the door gives it up (g.arrive, a word, g.receive). The door with nothing in hand is a
// word through it with whoever is at the other end: g.through, and a choose through the door.
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
// stands on the sand by the river; talking to him is `g.talk(CARRIER)`. The tree below uses every piece there is: a start
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
        { id: "jars", line: "proof.carrier.opt.jars", say: { 1: ["proof.carrier.jars.1"], 2: ["proof.carrier.jars.2"], more: ["proof.carrier.jars.more"] } },
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
        { id: "show", line: "proof.carrier.opt.show", say: ["proof.carrier.show.1"], do: fetchWater, then: "back" },
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
const party = (g) => !!g.flag("proof.party");
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
  walk: { area: [[352, 300], [640, 300], [780, 326], [780, 596], [60, 596], [150, 470], [240, 384], [312, 322]] },
  spawn: { default: [420, 572], critter: [478, 566], fromTrack: [496, 330] },   // (NEVADA-12E: the creature's own mark, and a way in from the track, for the party below)
  // NEVADA-12E: a party of two who are not family, while "proof.party" is true (see the top): Dad and the creature. A party
  // can be a function of the game, for one the story forms. By the way in from the track the creature arrives beside Dad.
  party: (g) => (party(g) ? ["dad", "critter"] : null),
  arrive: { fromTrack: [[540, 344]] },

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
  fx: [
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
  ],

  // Light that must stay smooth (a wormhole, a beam, a glow) is not painted. A scene draws it live, in the same pixels:
  //   live(art, g) { return art.portal(500, 300, 40, "door"); },        and a script finds it with g.q("#door")

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
    { id: "wagon", name: "wagon", poly: [[462, 492], [560, 470], [600, 420], [650, 388], [750, 394], [790, 440], [790, 520], [740, 544], [462, 520]], walkTo: [600, 574], face: "N", look: "egypt.wagon.look" },
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
      look: { critter: "proof.critter.dots", any: "proof.cooler.look" }, use: { critter: nibble, any: "proof.cooler.use.dad" } },
  ],

  // NEVADA-12E: Dad and the creature, talking (each exchange is what the one clicked on says, then what Dad makes of it)
  talk: {
    dad: { critter: [["proof.talk.dad.critter.1", "proof.critter.dots", "proof.talk.dad.critter.1b"]] },
    critter: { dad: [["proof.critter.dots", "proof.talk.critter.dad.1"]] },
  },
  given,

  // LETTERBOX-11: what the letterbox proof needs of the story when the scene is built: the two of them a team, the one who is
  // not here placed in another century, and the pack of gum in Dad's pockets, once. (And the proof's lines, for the tests.)
  setup(g) {
    for (const [id, line] of Object.entries(LINES)) if (!g.lines[id]) g.lines[id] = line;
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

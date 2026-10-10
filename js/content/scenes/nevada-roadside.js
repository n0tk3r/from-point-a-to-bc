// Act Four, its one scene: the middle of Nevada, the next morning, where the phone was last seen.
// Mom, Big Sister and Little Sister play, and the player switches between them.
//
// Two chains and a gate, and each of the three does what only she can:
//   Mom gets the witness to talk, by asking nicely and knowing her husband's car   (chain A)
//   ...and hands the coin he gives her to Big Sister, who can tell what it is       (chain A)
//   Little Sister asks the man in gray so many questions that he steps aside        (chain B)
//   ...and Big Sister reads the notice he was standing in front of                  (chain B)
//   the gate: whoever holds the coin flashes the morning sun off it, onto the place where the tracks stop
//
// The coin is the one the Son threw through the door in Rome: what goes into a door in one year comes out
// of one in another. And where the tire tracks stop there is a door too: shut, invisible, humming. Light
// opens a door, and the more light, the bigger the door. The old-timer saw it happen and does not know
// what he saw: the low sun flashed off the wagon's chrome, and the sky opened where the flash fell. The
// family do with a new silver coin what the wagon did by accident. A coin's worth of light: a coin's worth of door.
//
// The family's faith hangs on moments that were already here, and no puzzle knows of it (briefs/WEAVE.md):
//   the coin, when Big Sister reads it, is the coin of the tribute money, and Mom has the verse (Matthew 22:21)
//   before the coin goes up, Mom bows her head and the girls with her: a prayer in a line, and Little Sister's Amen
//   just before the reveal Little Sister asks what B.C. is, and is told
//   after "Daddy's EARLY", which stays the top of the scene, Mom has Psalm 31:15, and then the last two lines as they were
// And Little Sister's flashlight, which comes in her pocket from the house, gets its own answer where the tracks stop.
//
// The author's two rules of 7 October (briefs/DATING.md) hang on moments that were already here as well:
//   the years: the notice seals sectors 44 and 1921, every year before Christ is the Bible's own count, and 1921 B.C.
//     is on Big Sister's timeline, the year Abram went down into Egypt. Her mother knows the chapter. Big Sister sees,
//     once, that the doors open on years that matter, and does not know why.
//   the chickens: the old-timer's hens (told of, never seen) have stopped laying and face the fence; at the door it is
//     Little Sister who hears chickens, before anybody smells a sausage; and once she has heard of the hens, she
//     misses General Feathers.
//
// Try it: index.html?scene=nevada-roadside&lead=mom
// (to start at the last beat add &flags=nevada.arrived,nevada.witness,nevada.coinRead,nevada.distracted,nevada.notice,nevada.connected
//  and they will have no coin: for the coin, play it from the start.)

const art = "art/scenes/nevada-roadside/";

const each = (id) => ({ mom: `${id}.mom`, bigsis: `${id}.bigsis`, lilsis: `${id}.lilsis` });
const who = (g) => g.store.data.active;
/** Has this line been spoken yet? (The engine counts every line it says.) */
const heard = (g, id) => !!g.store.data.seenLines[id];
/** Does Big Sister hold both halves of the answer: what the coin is, and what the notice says? */
const ready = (g) => !!(g.flag("nevada.coinRead") && g.flag("nevada.notice"));
/** Head bowed, hands folded, each in her own way (Figure.pray in the engine). It is for someone standing still: let it go before she walks or reaches. */
const pray = (a, on) => a && a.pray && a.pray(on);
const THREE = ["mom", "bigsis", "lilsis"];

/** Once Big Sister has both the coin and the notice, she puts them together. Said once. */
async function connect(g) {
  if (ready(g) && !g.flag("nevada.connected")) {
    await g.say("nevada.connect");
    g.flag("nevada.connected", true);
  }
}

// ---------- the light ----------
// The door in time is where the tracks stop, in the air over the patch of fused sand: a ripple in the paint, the size
// of a coin (round ten: the engine's `portal`, in `fx` below), shut and unseen until the flash opens it. The light is
// drawn live (see `live` below): `#glint` is the spot of reflected sunlight, `#ray` the faint beam from the coin to it,
// and `#spark` the flash of the coin itself.
const PLACE = [646, 483];                                         // the painter's `over_the_glass`: where it hums
// Where they stand for the last beat. (The painter's marks "at the glass" put the three of them shoulder to shoulder,
// which suits one picture and not this scene: words go over a speaker's head, and Little Sister's head is lower than
// her mother's shoulder, so in a huddle whatever she says is written across the other two's faces. So the one with the
// coin stands alone at the near corner of the glass, an arm's length from the place; the two tall ones watch from the
// front row, well to the left; and Little Sister ends up beside the door, where her words sit clear above their heads.)
const HOLD = [572, 560];                                          // whoever has the coin
const BACK = { mom: [444, 590], bigsis: [488, 592], lilsis: [536, 580] };
const EYE = [616, 570];                                           // Little Sister, with her eye to the door: it is at the height of her eye

/** Where the coin is when one of them holds it out toward the place: in her hand, at the end of her arm.
    (Measured on each of them reaching: so far along, and so far up, as a share of her height.) */
const REACH = { mom: [0.37, 0.64], bigsis: [0.37, 0.64], lilsis: [0.37, 0.62] };
function hand(g) {
  const me = g.lead, tall = me.h * me.scale, [along, up] = REACH[me.id] || REACH.mom;      // (she is facing east: her arm is out to the right)
  return [me.x + along * tall, me.y - up * tall];
}
/** Put the spot of light at a place, with its beam from the coin. */
function aim(g, from, x, y) {
  const glint = g.q("#glint"), ray = g.q("#ray");
  if (glint) glint.setAttribute("transform", `translate(${x} ${y})`);
  if (ray) ray.setAttribute("points", `${from[0]},${from[1]} ${x - 1},${y - 4} ${x + 1},${y + 4}`);
}
/** Show or hide the three parts of the flash: the coin's own spark, the beam, and the spot where it lands. */
function shine(g, { spark = 0, ray = 0, glint = 0 } = {}, from = null) {
  const set = (id, opacity) => { const el = g.q(id); if (el) el.setAttribute("opacity", opacity); };
  set("#spark", spark); set("#ray", ray); set("#glint", glint);
  if (from) g.q("#spark")?.setAttribute("transform", `translate(${from[0]} ${from[1]})`);
}
/** How far open the door is: 0 is shut and not to be seen, 1 is the size of the coin. */
function openDoor(g, k) {
  const d = g.effects.get("door");
  if (d) d.open(k);
}

// ---------- chain A: the witness ----------
async function talkToOldTimer(g) {
  const me = who(g);
  if (me !== "mom") {
    const after = g.flag("nevada.witness") ? ".after" : "";
    const n = after ? (me === "bigsis" ? 3 : 2) : me === "bigsis" ? 4 : 3;
    return g.say(...Array.from({ length: n }, (_, i) => `nevada.old${after}.${me}.${i + 1}`));
  }
  if (!g.flag("nevada.witness")) {
    await g.say("nevada.old.mom.1", "nevada.old.mom.2", "nevada.old.mom.3", "nevada.old.mom.4", "nevada.old.mom.5", "nevada.old.mom.6", "nevada.old.mom.7");
    for (;;) {                                   // he wants to know she is who she says she is (a wrong answer costs a line, and he asks again)
      const pick = await g.choose([
        { id: "sedan", line: "nevada.car.sedan" },
        { id: "wagon", line: "nevada.car.wagon" },
        { id: "black", line: "nevada.car.black" },
      ]);
      await g.say(`nevada.car.${pick}`);
      if (pick === "wagon") break;
      await g.say(`nevada.car.no.${pick}`);
    }
    // What he saw. He does not know that the flash of light is the part that matters. And one more odd thing about the
    // week: his hens (behind the shack, never seen) have stopped laying, and face the fence. Little Sister knows what that means.
    await g.say("nevada.old.saw.1", "nevada.old.saw.1b", "nevada.old.saw.2", "nevada.old.saw.3", "nevada.old.saw.3b", "nevada.old.saw.3c", "nevada.old.saw.4", "nevada.old.saw.5");
    await g.reach();
    g.give("coin");
    g.flag("nevada.witness", true);
    return g.say("nevada.old.saw.6");
  }
  for (;;) {
    const pick = await g.choose([
      { id: "flash", line: "nevada.ask.flash" },
      { id: "fence", line: "nevada.ask.fence" },
      { id: "areas", line: "nevada.ask.areas" },
      { id: "bye", line: "nevada.ask.bye" },
    ]);
    await g.say(`nevada.ask.${pick}`, `nevada.ans.${pick}`);
    if (pick === "bye") return;
  }
}

async function readCoin(g) {
  await g.say("nevada.coin.read.1", "nevada.coin.read.2");
  // Caesar's own portrait: it is the coin of the tribute money. Little Sister knows it from Sunday school, Big Sister
  // has the fact, and Mom has the verse. Then back to what matters for the puzzle: the coin is new.
  await g.say("nevada.coin.read.2b", "nevada.coin.read.2c", "nevada.coin.read.2d");
  await g.say("nevada.coin.read.3", "nevada.coin.read.4");
  g.flag("nevada.coinRead", true);
  await connect(g);
}

// ---------- chain B: the man in gray, and what he is standing in front of ----------
async function talkToAgent(g) {
  const me = who(g);
  if (g.flag("nevada.distracted")) return me === "lilsis" ? g.say("nevada.agent.again.1", "nevada.agent.again.2") : g.say("nevada.agent.busy");
  // Mom's second try is General Washington's: courtesy, with the rule book named. It moves him no more than the first.
  if (me === "mom" && heard(g, "nevada.agent.mom.4")) return g.say("nevada.agent.mom.5", "nevada.agent.mom.6", "nevada.agent.mom.7");
  if (me !== "lilsis") return g.say(...[1, 2, 3, 4].map((n) => `nevada.agent.${me}.${n}`));
  await g.say("nevada.agent.lil.1", "nevada.agent.lil.2", "nevada.agent.lil.3", "nevada.agent.lil.4", "nevada.agent.lil.5", "nevada.agent.lil.6");
  // He retreats along the fence with a hand to his ear. She goes with him.
  const agent = g.actor("agent");
  agent.face("E");
  await Promise.all([g.moveTo(752, 468, "agent"), g.walkTo(708, 482)]);
  agent.face("E");
  g.lead.face("E");
  g.flag("nevada.distracted", true);
  await g.say("nevada.agent.lil.7", "nevada.agent.lil.8");
}

async function readNotice(g) {
  const me = who(g);
  if (!g.flag("nevada.distracted")) return g.say(`nevada.notice.blocked.${me}`);
  g.closeup(g.art.notice(), "The notice on the fence");
  if (me === "mom") return g.say("nevada.notice.mom.1", "nevada.notice.mom.2");
  if (me === "lilsis") return g.say("nevada.notice.lilsis");
  if (g.flag("nevada.notice")) return g.say("nevada.notice.again");
  await g.say("nevada.notice.big.1", "nevada.notice.big.2", "nevada.notice.big.3");
  g.flag("nevada.notice", true);
  g.closeup();
  await connect(g);
}

// ---------- the gate: where the tracks stop ----------

/** Going to the place. Until they know what they are looking at, Mom keeps them off it. After that there is
    nothing to see, and something to hear: whoever goes listens, and remembers what the old man said. */
async function atTheTracks(g) {
  const me = who(g);
  if (g.flag("demo.done")) return g.say("nevada.gate.6");        // (the door is open already: for whoever writes what comes next)
  if (!ready(g)) return g.say(`nevada.tracks.early.${me}`);
  await connect(g);
  if (heard(g, `nevada.hum.${me}.2`)) return g.say(`nevada.hum.${me}.2`);
  await g.say(`nevada.hum.${me}.1`, `nevada.hum.${me}.2`);
}

/** The coin, held up in the low sun. Whichever of them is holding it does this. */
async function flash(g) {
  const me = who(g);
  if (g.flag("demo.done")) return g.say("nevada.gate.6");        // it is open already, the size of the coin: the same light will not make it bigger
  if (!ready(g)) return g.say(`nevada.tracks.early.${me}`);
  await connect(g);
  // "Places, girls." The one with the coin goes to the corner of the glass. The other two stand back to watch.
  await g.say("nevada.gate.0");
  const others = THREE.filter((id) => id !== me);
  await Promise.all([g.walkTo(HOLD[0], HOLD[1]), ...others.map((id) => g.walkTo(BACK[id][0], BACK[id][1], id))]);
  for (const id of THREE) { const a = g.actor(id); if (a) a.face("E"); }
  await g.say("nevada.gate.1");
  // First things first. Mom bows her head, and the girls with her: nobody has to be told. A prayer in a line, in
  // her own words, and Little Sister's Amen. Then heads up and hands down, before anyone reaches or walks.
  pray(g.actor("mom"), true);
  await g.wait(280);
  for (const id of ["bigsis", "lilsis"]) pray(g.actor(id), true);
  await g.wait(420);
  await g.say("nevada.pray.1", "nevada.pray.2");
  for (const id of THREE) pray(g.actor(id), false);
  await g.wait(360);
  // The low morning sun. If it is Mom who has the coin, she knows of another one that was rising and not setting.
  if (me === "mom") await g.say("nevada.flash.sun");
  await g.say(`nevada.flash.${me}`);
  // The coin goes up into the sun, and flashes: once, onto the place that hums.
  const coin = hand(g), arm = g.reach();
  await g.wait(230);                                              // (her arm is out)
  aim(g, coin, PLACE[0], PLACE[1]);
  shine(g, { spark: 1, ray: 0.5, glint: 1 }, coin);
  await g.wait(170);                                              // (and held there)
  await g.tween(230, (k) => shine(g, { spark: 1 - k, ray: 0.5 * (1 - k), glint: 1 }));      // her arm comes down; the light stays where it fell
  await arm;
  // A coin's worth of light: a coin's worth of door.
  g.sfx("portal");
  await g.tween(900, (k) => { openDoor(g, k); shine(g, { glint: 1 - k }); }, g.ease.out);
  // The two tall ones take a step back. Little Sister has started before anybody can say no: it is the height of her eye.
  await Promise.all([g.walkTo(EYE[0], EYE[1], "lilsis"), ...["mom", "bigsis"].map((id) => g.walkTo(BACK[id][0], BACK[id][1], id))]);
  const lil = g.actor("lilsis");
  for (const id of THREE) { const a = g.actor(id); if (a) a.face("E"); }
  // What comes through it. Chickens first: Little Sister hears them before anybody smells a sausage, and her mother confirms her.
  await g.say("nevada.door.1", "nevada.door.2", "nevada.door.2b", "nevada.door.3", "nevada.door.4", "nevada.door.5", "nevada.door.6");
  // Both years. At the first of them, the Roman one, Little Sister asks what B.C. is, with her eye still at the door,
  // and her mother tells her: "before". The second is on Big Sister's timeline, the year Abram went down into Egypt, and
  // her mother knows the chapter. Then Big Sister sees that both are years that matter, and does not know why. A few
  // lines later Little Sister has done the sum her own way.
  await g.say("nevada.gate.2", "nevada.gate.2c", "nevada.gate.2d", "nevada.gate.2b", "nevada.gate.2e", "nevada.gate.2f", "nevada.gate.3");
  if (lil) lil.face("W");                                         // she turns round to them: she told them
  // The top of the scene is hers, word for word. Then Big Sister needs to sit down, Mom has the psalm, and the last two lines are as they were.
  await g.say("nevada.gate.4", "nevada.gate.5", "nevada.gate.5b", "nevada.gate.6", "nevada.gate.7");
  g.flag("demo.done", true);
  await g.wait(500);
  await g.fade(1, 900);
  await g.card("To be continued", "End of the demo", { plain: true, ms: 3200 });
  await g.title();
}

export default {
  id: "nevada-roadside",
  era: "nevada",
  name: "The last stop before nothing",

  // Every place in this file is the painter's own measurement of the finished picture (art/scenes/nevada-roadside/layout.json),
  // or was set by eye against the picture with the people standing in it; where the two differ the comment says why.

  // DEPTH. Out of doors, on flat ground that runs back to the foot of the mesas.
  horizon: 290, full: 590,

  // The dirt lot: from the car, bottom left, to the fence, and back as far as the shack's porch and the foot of the fence.
  walk: { area: [[0, 470], [40, 464], [104, 458], [150, 450], [262, 444], [270, 461], [410, 461], [414, 448], [540, 444], [600, 441], [640, 446], [760, 452], [800, 455], [800, 498], [738, 506], [722, 560], [652, 588], [600, 596], [0, 596]] },
  // The patch of sand that turned to glass. Nobody walks on it: Mom has said so.
  blocked: [[[580, 534], [600, 522], [640, 518], [690, 521], [714, 536], [690, 549], [640, 553], [602, 549]]],

  party: ["mom", "bigsis", "lilsis"],
  // They have just got out of the car, and stand looking at the place. (The painter's marks are a little lower and
  // closer together: 268, 572 for Mom, 318, 588 for Big Sister and 232, 554 for Little Sister. There the car's own
  // patch of ground takes Little Sister's place, and whatever she says is written across her mother's face, because
  // words go over a speaker's head and hers is the lowest. So the little one stands a row behind the other two.)
  spawn: { default: [286, 562], mom: [286, 562], bigsis: [334, 576], lilsis: [248, 528] },
  facing: "E",
  // No `edges` (round three: a way out across the edge of the picture). This scene has no way out: the car brought them,
  // and the only way on is the door in time where the tracks stop.

  picture: art + "back.png",
  planes: [
    { id: "pump", src: art + "pump.png", base: 452 },
    { id: "stand", src: art + "stand.png", base: 493, solid: [[410, 474], [546, 474], [548, 497], [408, 497]] },                  // the lemonade stand, and the ground under its table
    // Mom's car has come in from the left, and its tail is still off the edge of the picture.
    { id: "car", src: art + "car.png", base: [[0, 592], [225, 539]], solid: [[0, 535], [231, 535], [199, 596], [0, 596]] },
    { id: "front", src: art + "front.png", plane: "front" },      // the rusty drum and the sagebrush at the bottom right corner
    // Two that are not pictures: the patch of ground the man in gray is standing on. He moves when the story does, and
    // a cut-out's `solid` follows the story where a person's own does not.
    { id: "agent-ground", solid: [[641, 448], [681, 448], [681, 464], [641, 464]], when: (g) => !g.flag("nevada.distracted") },
    { id: "agent2-ground", solid: [[732, 458], [772, 458], [772, 474], [732, 474]], when: (g) => !!g.flag("nevada.distracted") },
  ],

  // LIGHT, drawn live. All of it starts out of sight: `setup` and the script `flash` bring it on.
  //   #ray     the faint beam from the coin to the spot
  //   #glint   the spot of reflected sunlight, on the place
  //   #spark   the flash of the coin itself, in her hand (she is drawn over it: what shows is what sticks out round her fist)
  //   (The door in time is not drawn here: it is the paint itself, bending, with a wet rim and a bright heart so that it
  //   shows on the sand in broad daylight. See `fx`.)
  live() {
    return `<defs>
        <radialGradient id="glint-glow"><stop offset="0" stop-color="#ffffff" stop-opacity="1"/><stop offset="0.4" stop-color="#fff3c2" stop-opacity="0.75"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>
      </defs>
      <polygon id="ray" points="0,0 0,0 0,0" fill="#fffbe6" opacity="0" shape-rendering="geometricPrecision"/>
      <g id="glint" opacity="0" shape-rendering="geometricPrecision"><circle r="15" fill="url(#glint-glow)"/><ellipse rx="4" ry="5" fill="#ffffff"/></g>
      <g id="spark" opacity="0" shape-rendering="geometricPrecision"><circle r="12" fill="url(#glint-glow)"/><path d="M-16,0 L16,0 M0,-16 L0,16" stroke="#ffffff" stroke-width="1.6" stroke-linecap="round"/></g>`;
  },

  // THINGS THAT MOVE BY NATURE (round four: briefs/out/paint-4b-ready.md): the two big birds that were painted still in
  // the sky cross it slowly now and then, and the old-timer has his coffee on: a thread of woodsmoke from the stovepipe,
  // nearly straight up in the still morning (the wind sock hangs slack: there is no wind).
  fx: [
    // The door in time (round ten): a ripple in the paint, the size of a coin, in the air over the glass where the tracks
    // stop; at its depth, the three of them at the glass are drawn in front of it, and the man along the fence behind.
    { id: "door", type: "portal", at: PLACE, r: 10, base: PLACE[1] + 1, pale: "#fffaf0", strength: 0.8 },      // (a coin door bends harder than the walk-in door, or it is not seen on the sand: the study's advice)
    { id: "birds", type: "birds", kind: "flyers", lanes: [[[-20, 168], [820, 128]], [[820, 54], [-20, 92]], [[-20, 112], [820, 70]]], every: [25, 55], group: [1, 2], speed: 34, color: "#2e3a5c", size: [7, 10],
      frames: { glide: "bird-0.png", flap: ["bird-1.png", "bird-0.png", "bird-2.png", "bird-0.png"], bank: "bird-3.png", middle: [7, 5.5] } },
    { id: "stovepipe", type: "smoke", at: [305.2, 279.7], base: 419, color: "#e6e2ea", opacity: 0.3, height: 46, width: [1.5, 7], lean: [4, -46], rate: 2 },
  ],

  // THEIR OWN LIVES (round four: js/engine/life.js).
  actors: [
    // He sits beside his table. (A seated person's place is the ground under the hips.) Now and then he gets up out of his
    // lawn chair, slowly (the chair stays put), and takes a few steps: back toward his pump and his shack, rubbing the
    // small of his back, or out in front to look down the road; and sits down again. His mark, against the end of his
    // stand, is off the ground the family walks on: he walks straight there and back.
    { id: "oldtimer", kind: "oldtimer", at: [388, 498], face: "SE",
      life: { every: [26, 48], spots: [[338, 468, "NE"], [372, 536, "SE"]], stay: [4, 8] } },
    // The man in gray: in front of the notice, and then a few yards along the fence. (The ground he stands on is among the cut-outs, above.)
    // While he is in front of the notice he keeps it covered (the story needs him there): small movements only, his
    // watch and his tie. Once he has stepped aside he paces a little along the fence, never back in front of it.
    { id: "agent", kind: "agent", at: [661, 458], face: "S", solid: false, when: (g) => !g.flag("nevada.distracted"),
      life: { still: true, fidget: [5, 11] } },
    { id: "agent", kind: "agent", at: [752, 468], face: "E", solid: false, when: (g) => !!g.flag("nevada.distracted"),
      life: { every: [18, 34], spots: [[726, 480, "W"], [784, 482, "E"]], stay: [2.5, 5] } },
  ],

  // Make the light match the story facts. Runs on arrival and after loading a save.
  setup(g) {
    shine(g);
    openDoor(g, g.flag("demo.done") ? 1 : 0);
  },

  // Back to front: a later area lies over an earlier one.
  // SHAPES (round three: the Show button outlines each thing, so each shape hugs its thing, a few pixels outside its edge).
  // They were traced from the painter's picture and cut-outs, and the old-timer and the man in gray from the figures the
  // engine draws at their marks. A thing that is a painted cut-out names it (`plane`): Show then outlines the cut-out's own
  // edge. The notice was already tight. The three of the family are clickable too (the engine puts an area over each one
  // standing here), so no shape lies over the places where they stand: where they arrive, and where they are sent to
  // stand (the places to stand below, and HOLD, BACK and EYE above). The check script holds it.
  hotspots: [
    { id: "shack", name: "shack", poly: [[128, 331], [166, 312], [166, 277], [203, 277], [204, 262], [211, 240], [220, 242], [216, 263], [216, 277], [279, 277], [279, 300], [299, 299], [300, 273], [311, 273], [311, 300], [348, 298], [348, 412], [327, 420], [326, 425], [312, 426], [262, 426], [132, 426], [128, 422]], walkTo: [254, 449], face: "N", look: each("nevada.shack") },      // its sign, its wind arrow and its stovepipe; down to its porch, and no lower (Mom's head is just under it when they arrive)
    { id: "fence", name: "fence", poly: [[562, 291], [614, 319], [800, 309], [800, 333], [617, 333], [617, 434], [606, 434], [603, 412], [562, 298]], walkTo: [590, 456], face: "N", look: each("nevada.fence") },      // its far side, its corner post, and the barbed wire along the top of its near side (the notice and the men are kept out of it)
    { id: "notice", name: "notice", verb: "Read", poly: [[630, 402], [695, 405], [695, 361], [630, 359]], walkTo: [646, 472], face: "N", look: readNotice, use: readNotice },
    { id: "pump", name: "gas pump", plane: "pump", poly: [[346, 348], [340, 352], [338, 357], [339, 364], [344, 370], [340, 372], [336, 378], [336, 433], [334, 442], [362, 443], [365, 439], [363, 428], [370, 426], [372, 422], [372, 392], [368, 385], [363, 384], [362, 374], [355, 370], [361, 361], [359, 352], [353, 348]], walkTo: [346, 466], face: "N", look: each("nevada.pump") },
    { id: "stand", name: "lemonade stand", plane: "stand", poly: [[490, 316], [486, 318], [485, 325], [413, 344], [416, 352], [428, 357], [437, 356], [448, 362], [463, 362], [478, 369], [474, 387], [474, 431], [471, 432], [467, 428], [452, 428], [444, 432], [443, 419], [431, 418], [424, 426], [423, 432], [415, 433], [416, 445], [420, 447], [420, 451], [428, 454], [423, 477], [426, 483], [425, 494], [428, 496], [431, 494], [435, 475], [439, 476], [439, 483], [449, 496], [453, 490], [472, 490], [475, 483], [480, 483], [486, 491], [503, 491], [507, 496], [512, 490], [513, 483], [522, 482], [525, 494], [531, 494], [522, 447], [537, 446], [539, 441], [530, 426], [524, 427], [520, 432], [516, 429], [490, 432], [480, 425], [483, 370], [485, 367], [491, 367], [501, 372], [518, 372], [526, 376], [539, 374], [544, 377], [551, 375], [553, 367], [492, 326], [493, 318]], walkTo: [486, 522], face: "N", look: each("nevada.stand") },      // its umbrella, its table and its sign
    {
      id: "oldtimer", name: "old-timer", verb: "Talk to", poly: [[372, 416], [371, 419], [377, 423], [379, 430], [366, 433], [369, 461], [367, 467], [370, 470], [370, 477], [365, 498], [368, 500], [372, 497], [378, 477], [386, 480], [384, 494], [391, 495], [393, 505], [406, 506], [410, 503], [421, 503], [423, 498], [419, 495], [418, 469], [413, 463], [400, 435], [394, 430], [394, 423], [399, 421], [401, 417], [388, 411]], walkTo: [432, 528], face: "NW",      // him and his chair, as the game draws them
      look: each("nevada.old.look"), use: talkToOldTimer, useWith: { coin: "nevada.old.coin" },
    },
    // The man in gray, before and after he backs off along the fence: Show outlines his own figure (the person "agent"), inside the area.
    {
      id: "agent", name: "man in gray", verb: "Talk to", poly: [[659, 365], [654, 368], [652, 373], [655, 379], [646, 384], [643, 398], [649, 403], [648, 458], [653, 462], [661, 455], [668, 462], [673, 458], [672, 403], [678, 398], [675, 384], [666, 379], [669, 376], [667, 368]], walkTo: [626, 476], face: "NE", when: (g) => !g.flag("nevada.distracted"),
      look: each("nevada.agent.look"), use: talkToAgent, useWith: { coin: ["nevada.agent.coin.1", "nevada.agent.coin.2"] },
    },
    {
      id: "agent2", name: "man in gray", verb: "Talk to", plane: "agent", actor: "agent", poly: [[750, 371], [744, 377], [746, 388], [736, 400], [736, 412], [745, 430], [746, 470], [757, 472], [761, 469], [761, 463], [757, 460], [757, 447], [763, 402], [760, 388], [763, 381], [759, 373]], walkTo: [708, 482], face: "E", when: (g) => !!g.flag("nevada.distracted"),
      look: each("nevada.agent.look"), use: talkToAgent, useWith: { coin: ["nevada.agent.coin.1", "nevada.agent.coin.2"] },
    },
    { id: "car", name: "Mom's car", plane: "car", poly: [[0, 423], [0, 582], [112, 582], [121, 586], [132, 586], [141, 582], [156, 582], [159, 580], [162, 569], [180, 569], [187, 564], [218, 523], [223, 520], [226, 505], [224, 486], [219, 475], [206, 466], [186, 460], [158, 457], [100, 425], [81, 421], [22, 421]], walkTo: [229, 588], face: "W", look: each("nevada.car.look") },
    {
      // The glass where the tracks stop, and the last stretch of the two ruts that run into it. The place that hums is in
      // the air over it: there is nothing there to click on but this. (The ruts higher up are left out: the family stand on
      // them and between them, to read the notice, to talk to the man in gray, and beside him once he has moved.)
      id: "tracks", name: "where the tracks stop", verb: "Go to", poly: [[595, 492], [613, 492], [604, 518], [694, 522], [693, 492], [709, 492], [711, 522], [726, 526], [738, 532], [740, 540], [733, 548], [700, 553], [650, 557], [620, 557], [590, 551], [572, 546], [560, 538], [558, 530], [566, 523], [585, 518]], walkTo: [548, 548], face: "E",
      // (Her flashlight, tried here: light is the right idea, and this is too little of it. Whoever holds it, she is the one who says so.)
      look: each("nevada.tracks.look"), use: atTheTracks, useWith: { coin: flash, lilflash: "nevada.tracks.lilflash" },
    },
  ],

  // Handing the coin over. Big Sister is the one who knows what it is. (The things they brought from the house can be
  // handed about too, and this scene has nothing to add: the game's own line is said, and that is all.)
  async given(g, item, to) {
    if (item !== "coin") return;
    if (to === "bigsis" && !g.flag("nevada.coinRead")) await readCoin(g);
    else if (to === "lilsis") await g.say("nevada.coin.lilsis");
    else if (to === "mom") await g.say("nevada.coin.mom");
  },

  talk: {
    mom: {
      bigsis: [
        { when: (g) => g.has("coin") && !g.flag("nevada.coinRead"), say: ["nevada.talk.mom.bigsis.coin.a", "nevada.talk.mom.bigsis.coin.b"] },
        { when: (g) => !!g.flag("nevada.coinRead"), say: ["nevada.talk.mom.bigsis.quarter.a", "nevada.talk.mom.bigsis.quarter.b"] },      // whose face is on the money, and what ours says
        ["nevada.talk.mom.bigsis.1a", "nevada.talk.mom.bigsis.1b"],
        ["nevada.talk.mom.bigsis.2a", "nevada.talk.mom.bigsis.2b", "nevada.talk.mom.bigsis.2c"],
      ],
      lilsis: [
        { when: (g) => !g.flag("nevada.distracted"), say: ["nevada.talk.mom.lilsis.gray.a", "nevada.talk.mom.lilsis.gray.b"] },
        ["nevada.talk.mom.lilsis.1a", "nevada.talk.mom.lilsis.1b"],
        ["nevada.talk.mom.lilsis.2a", "nevada.talk.mom.lilsis.2b"],
      ],
    },
    bigsis: {
      mom: [["nevada.talk.bigsis.mom.1a", "nevada.talk.bigsis.mom.1b"], ["nevada.talk.bigsis.mom.2a", "nevada.talk.bigsis.mom.2b", "nevada.talk.bigsis.mom.2c"]],
      lilsis: [
        { when: (g) => !g.flag("nevada.distracted"), say: ["nevada.talk.bigsis.lilsis.gray.a", "nevada.talk.bigsis.lilsis.gray.b"] },
        ["nevada.talk.bigsis.lilsis.1a", "nevada.talk.bigsis.lilsis.1b", "nevada.talk.bigsis.lilsis.1c", "nevada.talk.bigsis.lilsis.1d"],
        ["nevada.talk.bigsis.lilsis.2a", "nevada.talk.bigsis.lilsis.2b"],
      ],
    },
    lilsis: {
      mom: [
        // Once the old-timer has told of his hens, the next word she has with her mother is about her own chicken.
        { when: (g) => !!g.flag("nevada.witness"), say: ["nevada.talk.lilsis.mom.4a", "nevada.talk.lilsis.mom.4b"] },
        ["nevada.talk.lilsis.mom.1a", "nevada.talk.lilsis.mom.1b"], ["nevada.talk.lilsis.mom.2a", "nevada.talk.lilsis.mom.2b", "nevada.talk.lilsis.mom.2c"], ["nevada.talk.lilsis.mom.3a", "nevada.talk.lilsis.mom.3b"],
      ],
      bigsis: [["nevada.talk.lilsis.bigsis.1a", "nevada.talk.lilsis.bigsis.1b", "nevada.talk.lilsis.bigsis.1c"], ["nevada.talk.lilsis.bigsis.2a", "nevada.talk.lilsis.bigsis.2b", "nevada.talk.lilsis.bigsis.2c"]],
    },
  },

  async enter(g) {
    if (g.flag("nevada.arrived")) return;
    await g.wait(500);
    await g.say("nevada.arrive.1", "nevada.arrive.2", "nevada.arrive.2b", "nevada.arrive.3", "nevada.arrive.4");
    g.flag("nevada.arrived", true);
  },
};

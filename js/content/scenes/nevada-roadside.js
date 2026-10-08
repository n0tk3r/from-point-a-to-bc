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
// The door in time is where the tracks stop, in the air over the patch of fused sand. It is drawn live (see `live`
// below): `#door` is the door and `#hole` its rings; `#glint` is the spot of reflected sunlight, `#ray` the faint
// beam from the coin to it, and `#spark` the flash of the coin itself.
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
  const door = g.q("#door"), hole = g.q("#hole-all");
  if (door) door.setAttribute("opacity", k);
  if (hole) hole.style.transform = `scale(${Math.max(k, 0.01)})`;
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
  //   #door    the door in time, the size of a coin. Inside it, #hole is the game's own wormhole, very small, on a dark
  //            disc: out here in broad daylight the rings would not show against the sand without it.
  live(art) {
    const [x, y] = PLACE;
    return `<defs>
        <radialGradient id="glint-glow"><stop offset="0" stop-color="#ffffff" stop-opacity="1"/><stop offset="0.4" stop-color="#fff3c2" stop-opacity="0.75"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>
      </defs>
      <polygon id="ray" points="0,0 0,0 0,0" fill="#fffbe6" opacity="0" shape-rendering="geometricPrecision"/>
      <g id="door" opacity="0"><g id="hole-all" style="transform-origin:${x}px ${y}px">
        <circle cx="${x}" cy="${y}" r="11.5" fill="#140b2b" opacity="0.78" shape-rendering="geometricPrecision"/>
        <g class="flicker">${art.portal(x, y, 10, "hole")}</g>
      </g></g>
      <g id="glint" opacity="0" shape-rendering="geometricPrecision"><circle r="15" fill="url(#glint-glow)"/><ellipse rx="4" ry="5" fill="#ffffff"/></g>
      <g id="spark" opacity="0" shape-rendering="geometricPrecision"><circle r="12" fill="url(#glint-glow)"/><path d="M-16,0 L16,0 M0,-16 L0,16" stroke="#ffffff" stroke-width="1.6" stroke-linecap="round"/></g>`;
  },

  actors: [
    // He sits beside his table. (A seated person's place is the ground under the hips.)
    { id: "oldtimer", kind: "oldtimer", at: [388, 498], face: "SE" },
    // The man in gray: in front of the notice, and then a few yards along the fence. (The ground he stands on is among the cut-outs, above.)
    { id: "agent", kind: "agent", at: [661, 458], face: "S", solid: false, when: (g) => !g.flag("nevada.distracted") },
    { id: "agent", kind: "agent", at: [752, 468], face: "E", solid: false, when: (g) => !!g.flag("nevada.distracted") },
  ],

  // Make the light match the story facts. Runs on arrival and after loading a save.
  setup(g) {
    shine(g);
    openDoor(g, g.flag("demo.done") ? 1 : 0);
  },

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    { id: "shack", name: "shack", rect: [131, 240, 216, 192], walkTo: [254, 449], face: "N", look: each("nevada.shack") },
    { id: "fence", name: "fence", poly: [[583, 352], [583, 305], [612, 311], [800, 312], [800, 354], [627, 354], [627, 433], [612, 432]], walkTo: [590, 456], face: "N", look: each("nevada.fence") },
    { id: "notice", name: "notice", verb: "Read", poly: [[630, 402], [695, 405], [695, 361], [630, 359]], walkTo: [646, 472], face: "N", look: readNotice, use: readNotice },
    { id: "pump", name: "gas pump", rect: [334, 348, 40, 96], walkTo: [346, 466], face: "N", look: each("nevada.pump") },
    { id: "stand", name: "lemonade stand", rect: [415, 318, 137, 177], walkTo: [486, 522], face: "N", look: each("nevada.stand") },
    {
      id: "oldtimer", name: "old-timer", verb: "Talk to", rect: [360, 412, 62, 94], walkTo: [432, 528], face: "NW",      // him and his chair, as the game draws them (a little wider than the painter's stand-in)
      look: each("nevada.old.look"), use: talkToOldTimer, useWith: { coin: "nevada.old.coin" },
    },
    {
      id: "agent", name: "man in gray", verb: "Talk to", rect: [645, 366, 32, 96], walkTo: [626, 476], face: "NE", when: (g) => !g.flag("nevada.distracted"),
      look: each("nevada.agent.look"), use: talkToAgent, useWith: { coin: ["nevada.agent.coin.1", "nevada.agent.coin.2"] },
    },
    {
      id: "agent2", name: "man in gray", verb: "Talk to", rect: [736, 370, 32, 102], walkTo: [708, 482], face: "E", when: (g) => !!g.flag("nevada.distracted"),
      look: each("nevada.agent.look"), use: talkToAgent, useWith: { coin: ["nevada.agent.coin.1", "nevada.agent.coin.2"] },
    },
    { id: "car", name: "Mom's car", rect: [0, 423, 225, 162], walkTo: [229, 588], face: "W", look: each("nevada.car.look") },
    {
      // The ruts from the fence to the glass, and the glass. The place that hums is in the air over it: there is nothing there to click on but this.
      id: "tracks", name: "where the tracks stop", verb: "Go to", poly: [[604, 466], [712, 466], [732, 520], [730, 548], [650, 560], [566, 546], [564, 522]], walkTo: [548, 548], face: "E",
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
